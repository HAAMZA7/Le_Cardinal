# SKILL: Système 🖥️

Cette compétence permet au Cardinal de surveiller et de rapporter l'état de santé technique du PC.

## Description
Le Cardinal peut interroger les ressources système (CPU, RAM, Disque) et vérifier si les processus critiques (Watchdog, Chouette Veille) sont en cours d'exécution.

## Usage
- **Check Santé** : Exécuter `skills/systeme/check_sys.ps1`.
- **Diagnostic** : Analyser le JSON de sortie pour identifier les goulots d'étranglement.

## Instructions pour l'IA
Dès qu'Hamza demande "Comment va la machine ?" ou "État du système", lance le script PowerShell et fais une synthèse claire :
1.  **CPU** : [OK / Élevé]
2.  **RAM** : [Libre / Saturée]
3.  **Processus** : Liste les services critiques (`node`, `python`, `watchdog`).
4.  **Action** : Si la charge est > 80%, suggère de fermer des onglets ou des processus.
