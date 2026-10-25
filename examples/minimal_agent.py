#!/usr/bin/env python3
"""
minimal_agent.py — Démonstration pédagogique d'un agent LLM local à « function calling ».

Ce fichier illustre LA DÉMARCHE (boucle d'agent + appels d'outils validés) sur un
exemple générique et anodin. Il ne contient AUCUN code produit ni donnée réelle.

Idée clé : le modèle ne « raconte » pas une action — il demande l'exécution d'un
outil dont les arguments sont VALIDÉS avant exécution. Un argument manquant ou mal
typé est rejeté, jamais inventé. C'est ce qui rend un agent fiable plutôt que bavard.

Prérequis :
    - un serveur Ollama local (https://ollama.com)
    - un modèle supportant les outils, p.ex. :  ollama pull qwen3:4b-instruct
Dépendances : bibliothèque standard uniquement (urllib, json).
"""

import json
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434"
MODELE = "qwen3:4b-instruct"


class ErreurOutil(Exception):
    """Levée quand les arguments d'un outil ne respectent pas son schéma."""


def _post(chemin, charge, timeout=120):
    data = json.dumps(charge).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL + chemin,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def valider(args, schema):
    """Garde-fou : rejette un appel incomplet ou mal typé avant toute exécution."""
    props = schema.get("properties", {})
    for champ in schema.get("required", []):
        if champ not in args or args[champ] in (None, ""):
            raise ErreurOutil(f"champ obligatoire manquant : {champ}")
    for champ, valeur in args.items():
        attendu = props.get(champ, {}).get("type")
        if attendu == "number" and not isinstance(valeur, (int, float)):
            raise ErreurOutil(f"{champ} doit être un nombre")
        if attendu == "string" and not isinstance(valeur, str):
            raise ErreurOutil(f"{champ} doit être du texte")


# --- Un outil d'exemple, volontairement anodin -------------------------------

def convertir_temperature(valeur, unite):
    """Convertit une température entre Celsius et Fahrenheit (démonstration)."""
    u = unite.lower()
    if u in ("c", "celsius"):
        return f"{valeur} °C = {valeur * 9 / 5 + 32:.1f} °F"
    if u in ("f", "fahrenheit"):
        return f"{valeur} °F = {(valeur - 32) * 5 / 9:.1f} °C"
    return "ERREUR : unité inconnue (utiliser 'celsius' ou 'fahrenheit')"


OUTIL_TEMPERATURE = {
    "schema": {
        "type": "function",
        "function": {
            "name": "convertir_temperature",
            "description": "Convertit une température entre Celsius et Fahrenheit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "valeur": {"type": "number"},
                    "unite": {"type": "string", "description": "celsius ou fahrenheit"},
                },
                "required": ["valeur", "unite"],
            },
        },
    },
    "run": convertir_temperature,
}


# --- La boucle d'agent -------------------------------------------------------

def executer(message, outils, systeme=None, max_etapes=5):
    """Boucle : voir -> (appeler un outil validé -> réinjecter le résultat) -> conclure."""
    par_nom = {o["schema"]["function"]["name"]: o for o in outils}
    schemas = [o["schema"] for o in outils]

    messages = []
    if systeme:
        messages.append({"role": "system", "content": systeme})
    messages.append({"role": "user", "content": message})

    for _ in range(max_etapes):
        rep = _post("/api/chat", {
            "model": MODELE,
            "stream": False,
            "messages": messages,
            "tools": schemas,
        })
        msg = rep.get("message", {})
        messages.append(msg)

        appels = msg.get("tool_calls")
        if not appels:                       # pas d'outil demandé -> réponse finale
            return msg.get("content", "")

        for appel in appels:
            fn = appel["function"]
            nom = fn["name"]
            args = fn.get("arguments", {}) or {}
            if isinstance(args, str):
                args = json.loads(args)

            outil = par_nom.get(nom)
            if outil is None:
                res = f"ERREUR : outil inconnu {nom}"
            else:
                try:
                    valider(args, outil["schema"]["function"]["parameters"])
                    res = outil["run"](**args)
                except ErreurOutil as e:
                    res = f"ERREUR DE VALIDATION : {e}"
                except Exception as e:  # noqa: BLE001 — démo : on renvoie l'erreur au modèle
                    res = f"ERREUR D'EXÉCUTION : {e}"

            messages.append({"role": "tool", "tool_name": nom, "content": str(res)})

    return "(limite d'étapes atteinte)"


if __name__ == "__main__":
    SYSTEME = (
        "Tu es un assistant de démonstration. Réponds en français. "
        "Utilise l'outil de conversion quand c'est pertinent ; n'invente jamais de valeur."
    )
    question = "Il fait 25 degrés Celsius, ça fait combien en Fahrenheit ?"
    print(">>>", question)
    print(executer(question, outils=[OUTIL_TEMPERATURE], systeme=SYSTEME))
