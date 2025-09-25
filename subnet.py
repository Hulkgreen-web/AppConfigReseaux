import ipaddress
import math

def is_masque_valide(masque):
    try:
        # Découpe du masque en octets
        octets = masque.split('.')
        if len(octets) != 4:
            return False

        #Vérification que chaque octet est entre 0 et 255
        valeurs = []

        for octet in octets:
            if not octet.isdigit():
                return False
            v = int(octet)
            if v < 0 or v > 255:
                return False
            valeurs.append(v)

        #Conversion du masque en binaire
        binaire = "".join(f"{v:08b}" for v in valeurs)

        #Vérifier que le masque est un suite de 1 suivie d'une suite de 0
        if "01" in binaire:
            i = binaire.index("01")
            # Après le 01, plus de 1
            if "1" in binaire[i + 2]:
                return False
        # On exclu les masques 0.0.0.0 et 255.255.255.255
        if not ("1" in binaire and "0" in binaire):
            return False

        return True
    except Exception:
        return False

def masque_pointee_to_cidr(masque_pointee):
    """
    Convertit un masque en notation pointée en notation CIDR

    :param masque_pointee: Masque réseau en notation pointée (ex: 255.255.255.0)
    :return: Notation CIDR (ex: 24)
    """

    if is_masque_valide(masque_pointee):
        # Convertir le masque pointée en binaire
        binary_mask = ''.join([bin(int(x))[2:].zfill(8) for x in masque_pointee.split('.')])

        # Compter le nombre de 1 dans le masque binaire
        return binary_mask.count('1')
    else:
        raise ValueError("Masque invalide")

def decoupage_classique(adresse_ip, masque_pointee, nombre_sr):
    """
    Réalise un découpage classique en sous-réseaux de taille identique

    :param adresse_ip: Adresse IP du réseau (notation pointée)
    :param masque_pointee: Masque de réseau (notation pointée)
    :param nombre_sr: Nombre de sous-réseaux souhaités
    """

    # Convertir le masque pointée en notation CIDR
    masque_cidr = masque_pointee_to_cidr(masque_pointee)

    # Créer le réseau initial
    reseau_initial = ipaddress.IPv4Network(f"{adresse_ip}/{masque_cidr}", strict=False)

    # Calculer le nombre de bits à emprunter pour le nombre de sous-réseaux
    bits_emprunt = math.ceil(math.log2(nombre_sr))

    # Nouveau masque de sous-réseau
    nouveau_masque = reseau_initial.prefixlen + bits_emprunt

    # Vérifier la validité du découpage
    if nouveau_masque > 30:
        raise ValueError("Impossible de créer autant de sous-réseaux")

    # Générer les sous-réseaux
    sous_reseaux = list(reseau_initial.subnets(new_prefix=nouveau_masque))

    return sous_reseaux[:nombre_sr]


def generer_plan_adressage_classique(adresse_ip, masque, nombre_sr):
    """
    Génère un plan d'adressage pour un découpage classique
    """
    sous_reseaux = decoupage_classique(adresse_ip, masque, nombre_sr)

    plan_adressage = {}
    for i, sr in enumerate(sous_reseaux, 1):
        # Calculer le nombre d'hôtes par sous-réseau
        hotes_par_sr = sr.num_addresses - 2  # Soustrait réseau et broadcast

        plan_adressage[f"SR{i}"] = {
            "Réseau": str(sr.network_address),
            "Masque": str(sr.netmask),
            "Nombre total d'adresses": hotes_par_sr,
            "Première IP utilisable": str(sr[1]),
            "Dernière IP utilisable": str(sr[-2]),
            "Adresse de broadcast": str(sr[-1])
        }

    return plan_adressage