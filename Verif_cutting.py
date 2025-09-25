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
        nb_ips = 2 ** bits_hotes - 2
        return True, f"Possible : chaque SR aura {nb_ips} IPs utilisables."
    elif nb_ips_par_sr is not None:
        if nb_ips_par_sr <= 0:
            return False, "Erreur : nombre d'IPs doit être positif."
        bits_hotes = nb_bits_necessaires(nb_ips_par_sr + 2)
        if bits_hotes > bits_disponibles:
            return False, "Impossible : pas assez de bits pour ce nombre d'IPs par SR."
        bits_sr = bits_disponibles - bits_hotes
        nb_sr_possibles = 2 ** bits_sr
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

# --- Interface graphique ---
def calculer_classique():
    ip = entry_ip.get()
    masque = entry_masque.get()
    choix = var_choix.get()
    if choix == 1:
        try:
            nb_sr = int(entry_nb_sr.get())
        except:
            messagebox.showerror("Erreur", "Nombre de sous-réseaux invalide.")
            return
        ok, msg = verifier_decoupe_classique(ip, masque, nb_sr=nb_sr)
    else:
        try:
            nb_ips = int(entry_nb_ips.get())
        except:
            messagebox.showerror("Erreur", "Nombre d'IPs invalide.")
            return
        ok, msg = verifier_decoupe_classique(ip, masque, nb_ips_par_sr=nb_ips)
    if ok:
        messagebox.showinfo("Résultat", msg)
    else:
        messagebox.showerror("Erreur", msg)

def calculer_vlsm():
    ip = entry_ip_vlsm.get()
    masque = entry_masque_vlsm.get()
    besoins_str = entry_besoins.get()
    try:
        besoins = [int(x) for x in besoins_str.split(",")]
    except:
        messagebox.showerror("Erreur", "Liste des besoins invalide (ex: 50,20,10)")
        return
    ok, msg = verifier_vlsm_possible(ip, masque, besoins)
    if ok:
        messagebox.showinfo("Résultat", msg)
    else:
        messagebox.showerror("Erreur", msg)

# --- Fenêtre principale avec thème et fond ---
root = ThemedTk(theme="arc")
root.title("Outil de découpe réseau")
root.geometry("500x450")
root.configure(bg="#cce0ff")  # Bleu plus foncé

# --- Style des champs de saisie ---
entry_style = {"background": "#f0f0f0"}  # Gris clair

# --- Découpe classique ---
frame1 = ttk.LabelFrame(root, text="Découpe classique", padding=10)
frame1.pack(padx=10, pady=10, fill="x")

ttk.Label(frame1, text="Adresse IP de base :").grid(row=0, column=0, sticky="e")
entry_ip = tk.Entry(frame1, **entry_style)
entry_ip.grid(row=0, column=1)

ttk.Label(frame1, text="Masque (ex: 24 ou 255.255.255.0) :").grid(row=1, column=0, sticky="e")
entry_masque = tk.Entry(frame1, **entry_style)
entry_masque.grid(row=1, column=1)

var_choix = tk.IntVar(value=1)
ttk.Radiobutton(frame1, text="Nombre de sous-réseaux", variable=var_choix, value=1).grid(row=2, column=0, sticky="w")
entry_nb_sr = tk.Entry(frame1, **entry_style)
entry_nb_sr.grid(row=2, column=1)

ttk.Radiobutton(frame1, text="Nombre d'IPs par SR", variable=var_choix, value=2).grid(row=3, column=0, sticky="w")
entry_nb_ips = tk.Entry(frame1, **entry_style)
entry_nb_ips.grid(row=3, column=1)

ttk.Button(frame1, text="Vérifier", command=calculer_classique).grid(row=4, column=0, columnspan=2, pady=5)

# --- VLSM ---
frame2 = ttk.LabelFrame(root, text="Vérification VLSM", padding=10)
frame2.pack(padx=10, pady=10, fill="x")

ttk.Label(frame2, text="Adresse IP de base :").grid(row=0, column=0, sticky="e")
entry_ip_vlsm = tk.Entry(frame2, **entry_style)
entry_ip_vlsm.grid(row=0, column=1)

ttk.Label(frame2, text="Masque (ex: 24 ou 255.255.255.0) :").grid(row=1, column=0, sticky="e")
entry_masque_vlsm = tk.Entry(frame2, **entry_style)
entry_masque_vlsm.grid(row=1, column=1)

ttk.Label(frame2, text="Besoins en IPs par SR (ex: 50,20,10) :").grid(row=2, column=0, sticky="e")
entry_besoins = tk.Entry(frame2, **entry_style)
entry_besoins.grid(row=2, column=1)

ttk.Button(frame2, text="Vérifier VLSM", command=calculer_vlsm).grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()