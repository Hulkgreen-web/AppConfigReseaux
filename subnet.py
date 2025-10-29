import ipaddress
import math

def is_ip_valide(adresse_ip):
    try:
        # vérification du format de l'adresse IP
        octets = adresse_ip.split(".")
        if len(octets) != 4:
            return False

        # Vérification que chaque octet est un nombre et est entre 0 et 255
        for octet in octets:
            if not octet.isdigit():
                return False
            v = int(octet)
            if v < 0 or v > 255:
                return False

            # Utilisation de la méthode IPv4Address pour une vérification supplémentaire
            ipaddress.IPv4Address(adresse_ip)
            return True
    except (ValueError, AttributeError, TypeError):
        return False


def is_adresse_reseau_valide(adresse_ip, masque_pointee):
    """
    Vérifie si l'adresse IP est une adresse de réseau valide avec le masque donné

    :param adresse_ip: Adresse IP à vérifier
    :param masque_pointee: Masque réseau
    :return: Tuple (bool, str) indiquant si valide et message d'erreur le cas échéant
    """
    try:
        # Convertir le masque en CIDR
        masque_cidr = masque_pointee_to_cidr(masque_pointee)

        # Créer le réseau
        reseau = ipaddress.IPv4Network(f"{adresse_ip}/{masque_cidr}", strict=True)

        # Vérifier si l'adresse IP correspond à l'adresse réseau
        if str(reseau.network_address) != adresse_ip:
            return False, f"L'adresse {adresse_ip} n'est pas une adresse de réseau valide avec le masque {masque_pointee}. L'adresse réseau devrait être {reseau.network_address}"

        return True, "Adresse de réseau valide"

    except ValueError as e:
        return False, f"Adresse réseau invalide: {str(e)}"


def analyse_adresse_ip(adresse_ip, masque_pointee=None):
    """
    Analyse complète d'une adresse IP et retourne des informations détaillées

    :param adresse_ip: Adresse IP à analyser
    :param masque_pointee: Masque réseau optionnel pour l'analyse
    :return: Dictionnaire avec l'analyse complète
    """
    analyse = {
        "adresse_ip": adresse_ip,
        "valide": False,
        "type": "Inconnu",
        "classe": "Inconnue",
        "reseau_prive": False,
        "message_erreur": "",
        "details": {}
    }

    # Validation basique de l'adresse IP
    valide = is_ip_valide(adresse_ip)
    if not valide:
        return analyse

    analyse["valide"] = True

    try:
        ip_obj = ipaddress.IPv4Address(adresse_ip)

        # Déterminer la classe de l'adresse IP
        premier_octet = int(adresse_ip.split('.')[0])
        if 1 <= premier_octet <= 126:
            analyse["classe"] = "A"
        elif 128 <= premier_octet <= 191:
            analyse["classe"] = "B"
        elif 192 <= premier_octet <= 223:
            analyse["classe"] = "C"
        elif 224 <= premier_octet <= 239:
            analyse["classe"] = "D (Multicast)"
        elif 240 <= premier_octet <= 255:
            analyse["classe"] = "E (Réservée)"

        # Déterminer le type d'adresse
        if ip_obj.is_private:
            analyse["type"] = "Privée"
            analyse["reseau_prive"] = True
        elif ip_obj.is_loopback:
            analyse["type"] = "Loopback"
        elif ip_obj.is_multicast:
            analyse["type"] = "Multicast"
        elif ip_obj.is_global:
            analyse["type"] = "Publique"
        elif ip_obj.is_reserved:
            analyse["type"] = "Réservée"
        elif ip_obj.is_unspecified:
            analyse["type"] = "Non spécifiée"
        elif ip_obj.is_link_local:
            analyse["type"] = "Link-local"

        # Analyse avec masque si fourni
        if masque_pointee:
            valide_reseau, message_reseau = is_adresse_reseau_valide(adresse_ip, masque_pointee)
            analyse["reseau_valide"] = valide_reseau
            analyse["message_reseau"] = message_reseau

            if valide_reseau:
                masque_cidr = masque_pointee_to_cidr(masque_pointee)
                reseau = ipaddress.IPv4Network(f"{adresse_ip}/{masque_cidr}", strict=True)

                analyse["details"].update({
                    "adresse_reseau": str(reseau.network_address),
                    "masque_cidr": masque_cidr,
                    "plage_hotes": f"{reseau.num_addresses - 2}",
                    "premiere_ip": str(reseau[1]),
                    "derniere_ip": str(reseau[-2]),
                    "broadcast": str(reseau.broadcast_address)
                })

        return analyse

    except Exception as e:
        analyse["valide"] = False
        analyse["message_erreur"] = f"Erreur lors de l'analyse: {str(e)}"
        return analyse

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

    analyse_ip = analyse_adresse_ip(adresse_ip,masque_pointee)

    if not analyse_ip["valide"]:
        raise ValueError(f"Adresse IP invalide: {adresse_ip}")

    if analyse_ip["type"] in ["Loopback", "Multicast"]:
        raise ValueError(f"Impossible de découper une adresse de type {analyse_ip['type']}")

    valide_masque = is_masque_valide(masque_pointee)
    if not valide_masque:
        raise ValueError("Masque valide")

    if not analyse_ip.get("reseau_valide", False):
        raise ValueError(f"Adresse IP invalide: {adresse_ip}, L'adresse n'est pas une adresse de réseau valide avec ce masque")

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

        plan_adressage[i] = {
            "Réseau": str(sr.network_address),
            "Masque": str(sr.netmask),
            "Nombre total d'adresses": hotes_par_sr,
            "Première IP utilisable": str(sr[1]),
            "Dernière IP utilisable": str(sr[-2]),
            "Adresse de broadcast": str(sr[-1])
        }

    return plan_adressage