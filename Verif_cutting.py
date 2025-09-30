import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk, messagebox
import math
import ipaddress

# --- Fonctions de calcul ---
def nb_bits_necessaires(valeur):
    return math.ceil(math.log2(valeur))

def verifier_decoupe_classique(ip_reseau, masque, nb_sr=None, nb_ips_par_sr=None):
    try:
        reseau = ipaddress.IPv4Network(f"{ip_reseau}/{masque}", strict=False)
    except Exception:
        return False, "Erreur : IP ou masque invalide."

    bits_disponibles = 32 - reseau.prefixlen

    if nb_sr is not None:
        if nb_sr <= 0:
            return False, "Erreur : nombre de sous-réseaux doit être positif."
        bits_sr = nb_bits_necessaires(nb_sr)
        if bits_sr > bits_disponibles:
            return False, "Impossible : pas assez de bits pour ce nombre de sous-réseaux."
        bits_hotes = bits_disponibles - bits_sr
        nb_ips = pow(2,bits_hotes) - 2
        return True, f"Possible : chaque SR aura {nb_ips} IPs utilisables."
    elif nb_ips_par_sr is not None:
        if nb_ips_par_sr <= 0:
            return False, "Erreur : nombre d'IPs doit être positif."
        bits_hotes = nb_bits_necessaires(nb_ips_par_sr + 2)
        if bits_hotes > bits_disponibles:
            return False, "Impossible : pas assez de bits pour ce nombre d'IPs par SR."
        bits_sr = bits_disponibles - bits_hotes
        nb_sr_possibles = pow(2,bits_sr)
        return True, f"Possible : on peut faire {nb_sr_possibles} sous-réseaux."
    else:
        return False, "Erreur : il faut spécifier nb_sr ou nb_ips_par_sr."

def verifier_vlsm_possible(ip_reseau, masque, besoins_ips):
    try:
        reseau = ipaddress.IPv4Network(f"{ip_reseau}/{masque}", strict=False)
    except Exception:
        return False, "Erreur : IP ou masque invalide."

    nb_ips_total = 2 ** (32 - reseau.prefixlen) - 2

    total_utilise = 0
    for besoin in besoins_ips:
        if besoin <= 0:
            return False, "Erreur : tous les besoins doivent être positifs."
        taille_bloc = 2 ** nb_bits_necessaires(besoin + 2)
        total_utilise += taille_bloc

    if total_utilise <= nb_ips_total:
        return True, f"Possible : total utilisé = {total_utilise}, total dispo = {nb_ips_total}"
    else:
        return False, f"Impossible : total utilisé = {total_utilise}, total dispo = {nb_ips_total}"

