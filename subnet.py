import ipaddress
import math


def masque_pointee_to_cidr(masque_pointee):
    """
    Convertit un masque en notation pointée en notation CIDR

    :param masque_pointee: Masque réseau en notation pointée (ex: 255.255.255.0)
    :return: Notation CIDR (ex: 24)
    """
    # Convertir le masque pointée en binaire
    binary_mask = ''.join([bin(int(x))[2:].zfill(8) for x in masque_pointee.split('.')])

    # Compter le nombre de 1 dans le masque binaire
    return binary_mask.count('1')

def decoupage_classique(adresse_ip, masque_pointee, nombre_sr):
    """
    Réalise un découpage classique en sous-réseaux de taille identique

    :param adresse_ip: Adresse IP du réseau (notation pointée)
    :param masque: Masque de réseau (notation CIDR)
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


# Exemple d'utilisation
def main():
    # Paramètres de configuration
    adresse_ip = "192.168.1.0"  # Réseau principal
    masque = "255.255.255.0"  # Masque /24
    nombre_sr = 8  # Nombre de sous-réseaux souhaités

    try:
        # Générer le plan d'adressage
        plan = generer_plan_adressage_classique(adresse_ip, masque, nombre_sr)

        # Afficher le plan d'adressage
        print("Plan d'adressage des sous-réseaux (découpage classique) :")
        for sr, details in plan.items():
            print(f"\n{sr}:")
            for cle, valeur in details.items():
                print(f"  {cle}: {valeur}")

    except ValueError as e:
        print(f"Erreur : {e}")


# Exécution du script
if __name__ == "__main__":
    main()
