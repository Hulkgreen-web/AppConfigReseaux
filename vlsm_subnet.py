import math
class VLSMSimple:
    def __init__(self):
        self.subnets = []

    def ip_to_int(self, ip):
        """Convertit une adresse IP en entier"""
        octets = ip.split('.')
        return (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])

    def int_to_ip(self, ip_int):
        """Convertit un entier en adresse IP"""
        return f"{(ip_int >> 24) & 0xff}.{(ip_int >> 16) & 0xff}.{(ip_int >> 8) & 0xff}.{ip_int & 0xff}"

    def cidr_to_mask(self, cidr):
        """Convertit CIDR en masque décimal. Accepte 24 ou '/24'."""
        # Accepter int ou str (avec ou sans '/')
        if isinstance(cidr, str):
            cidr = cidr.lstrip('/')  # enlève leading '/' s'il existe
        cidr = int(cidr)  # lève ValueError si non numérique

        mask_int = (0xffffffff << (32 - cidr)) & 0xffffffff
        return self.int_to_ip(mask_int)

    def calculer_vlsm(self, ip_depart, masque_cidr, nombre_sous_reseaux, liste_ips):
        """
        ip_depart: str (adresse de départ)
        masque_cidr: int (ex: 24)
        nombre_sous_reseaux: int (nombre attendu de sous-réseaux)
        liste_ips: iterable d'entiers (nombre d'IPs requises pour chaque sous-réseau)
        Retour: liste de dicts pour chaque sous-réseau (allocation dans l'ordre d'allocation)
        """

        if not isinstance(nombre_sous_reseaux, int) or nombre_sous_reseaux <= 0:
            raise ValueError("nombre_sous_reseaux doit être un entier > 0")

        liste_ips = list(liste_ips)
        if len(liste_ips) != nombre_sous_reseaux:
            raise ValueError("La longueur de liste_ips doit être égale à nombre_sous_reseaux")

        print(f"\n{'=' * 60}")
        print("CALCUL VLSM")
        print(f"{'=' * 60}")
        print(f"Réseau de base: {ip_depart}/{masque_cidr}")
        print(f"Masque: {self.cidr_to_mask(masque_cidr)}")

        # Vérifier l'adresse réseau
        reseau_base = self.calculer_adresse_reseau(ip_depart, self.cidr_to_mask(masque_cidr))
        if reseau_base != ip_depart:
            print(f"⚠️  Adresse réseau corrigée: {reseau_base}")
            ip_depart = reseau_base

        # Préparer la liste en gardant l'indice d'origine pour rapporter la demande initiale
        sous_reseaux_demande = [
            {'index_orig': idx + 1, 'ips_requises': ips}
            for idx, ips in enumerate(liste_ips)
        ]

        # Trier par ips_requises décroissant pour allocation VLSM
        sous_reseaux_demande.sort(key=lambda x: x['ips_requises'], reverse=True)
        print(f"\nSous-réseaux (ordre décroissant des besoins): {[s['ips_requises'] for s in sous_reseaux_demande]}")

        # Vérifier CIDR
        if not (0 <= masque_cidr <= 32):
            raise ValueError("Masque CIDR invalide")

        current_ip = ip_depart
        results = []

        for allocation_num, s in enumerate(sous_reseaux_demande, 1):
            required_ips = s['ips_requises']
            print(f"\n--- Allocation {allocation_num} (demande origine #{s['index_orig']}: {required_ips} IPs) ---")
            print(f"Adresse départ: {current_ip}")

            total_needed = required_ips + 2
            host_bits = math.ceil(math.log2(total_needed))
            new_cidr = 32 - host_bits
            block_size = 2 ** host_bits

            network_ip = current_ip
            network_int = self.ip_to_int(network_ip)
            broadcast_int = network_int + block_size - 1
            first_ip_int = network_int + 1
            last_ip_int = broadcast_int - 1

            broadcast_ip = self.int_to_ip(broadcast_int)
            first_ip = self.int_to_ip(first_ip_int)
            last_ip = self.int_to_ip(last_ip_int)
            subnet_mask = self.cidr_to_mask(new_cidr)
            usable_ips = block_size - 2

            subnet_info = {
                'numero_allocation': allocation_num,
                'index_origine': s['index_orig'],
                'reseau': network_ip,
                'masque': subnet_mask,
                'cidr': new_cidr,
                'premiere_ip': first_ip,
                'derniere_ip': last_ip,
                'broadcast': broadcast_ip,
                'ips_utilisables': usable_ips,
                'ips_requises': required_ips,
                'taille_bloc': block_size
            }
            results.append(subnet_info)

            print(
                f"Réseau: {network_ip}/{new_cidr}  | Plage: {first_ip} - {last_ip}  | Broadcast: {broadcast_ip}  | IPs utilisables: {usable_ips}")

            # Préparer pour le suivant
            current_ip = self.int_to_ip(broadcast_int + 1)
            print(f"Prochaine adresse: {current_ip}")

        # Optionnel: trier results par index_origine si vous voulez retrouver l'ordre demandé initial
        # results.sort(key=lambda x: x['index_origine'])
        return results

    def calculer_adresse_reseau(self, ip, masque):
        """Calcule l'adresse réseau"""
        ip_int = self.ip_to_int(ip)
        masque_int = self.ip_to_int(masque)
        reseau_int = ip_int & masque_int
        return self.int_to_ip(reseau_int)