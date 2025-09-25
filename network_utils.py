import ipaddress

#"str" pour string car les données rentrée par l'utilisateur sont des string
#classless par defaut si pas précisé par l'utilisateur

#Point 1
def calculate_network_info(ip_str, mask_str, mode='classless'):

    try:
        if mode == 'classless':
            # Accepte /24 ou masque décimal
            # network contient l'ip et le masque concaténé ex  : 192.168.5.1/24
            if '/' in mask_str:
                network = ipaddress.ip_network(ip_str + mask_str, strict=False)
            else:
                # Convertit masque décimal en CIDR si possible
                network = ipaddress.ip_network(f"{ip_str}/{mask_str}", strict=False)

        # calcule de l'adress réseau et de broadcast en classfull
        elif mode == 'classful':
            ip = ipaddress.ip_address(ip_str)
            first_octet = int(ip_str.split('.')[0])
            mask = 8 if 0 <= first_octet <= 127 else 16 if 128 <= first_octet <= 191 else 24
            network = ipaddress.ip_network(f"{ip_str}/{mask}", strict=False)

        else:
            return {"erreur": "Mode invalide : 'classless' ou 'classful' attendu"}

        result = {
            'adresse réseau': str(network.network_address),
            'adresse de brocast': str(network.broadcast_address),
            'masque de sous réseau': str(network.netmask)
        }

        # Sous-réseau si masque > classe standard en classful
        if mode == 'classful':
            class_mask = 8 if first_octet <= 127 else 16 if first_octet <= 191 else 24
            if network.prefixlen > class_mask:
                result['subnet'] = f"{str(network.network_address)}/{network.prefixlen}"
            else:
                result['subnet'] = "N/A"
        else:  # classless
            result['subnet'] = f"{str(network.network_address)}/{network.prefixlen}"
        return result
    except ValueError as e:
        return {"error": f"IP ou masque invalide : {e}"}


#Point 2
def check_ip_belongs(ip_to_check, network_ip, mask_str, mode='classless'):
    try:
        # Réutilise la fonction calculate_network_info pour obtenir les informations de base
        network = calculate_network_info(network_ip, mask_str, mode)
        if 'error' in network:
            return network

        # Détermine l'objet réseau en fonction du mode
        if mode == 'classless':
            network_obj = ipaddress.ip_network(f"{network_ip}/{mask_str}", strict=False)
        else:  # mode == 'classful'
            first_octet = int(network_ip.split('.')[0])
            if 0 <= first_octet <= 127:
                mask = 8
            elif 128 <= first_octet <= 191:
                mask = 16
            else:  # 192 <= first_octet <= 223
                mask = 24
            network_obj = ipaddress.ip_network(f"{network_ip}/{mask}", strict=False)

        # Vérifie l'appartenance de l'IP et calcule les hôtes
        ip = ipaddress.ip_address(ip_to_check)
        belongs = ip in network_obj
        hosts = list(network_obj.hosts())

        return {
            'appartient': belongs,
            'premier hote': str(hosts[0]) if hosts else "Aucun hôte",
            'dernier hote': str(hosts[-1]) if hosts else "Aucun hôte"
        }
    except ValueError as e:
        return {"error": f"IP ou masque invalide : {e}"}
# Tests statiques
if __name__ == "__main__":
    print("=== Point 1 ===")
    print(calculate_network_info("192.168.1.100", "24", "classless"))
    print(calculate_network_info("10.0.0.1", "16", "classful"))  # Masque ignoré, classe A
    print(calculate_network_info("999.999.999.999", "24", "classless"))  # Erreur

    print("\n=== Point 2 ===")
    print(check_ip_belongs("192.168.1.50", "192.168.1.0", "24", "classless"))
    print(check_ip_belongs("10.0.0.50", "192.168.1.0", "24", "classless"))