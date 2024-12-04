import dns.resolver

def query_dns(domain, record_type="A", dns_server="114.114.114.114", port=53):
    """
    查询指定域名的 DNS 记录，支持自定义 DNS 服务器和端口。
    
    :param domain: 要查询的域名。
    :param record_type: 要查询的记录类型（例如 A、AAAA、MX、NS 等）。
    :param dns_server: 自定义 DNS 服务器地址（默认使用 Google 公共 DNS）。
    :param port: 自定义 DNS 服务器端口（默认 53）。
    :return: 查询结果。
    """
    try:
        # 创建解析器
        resolver = dns.resolver.Resolver()
        
        # 设置自定义 DNS 服务器和端口
        resolver.nameservers = [dns_server]
        resolver.port = port
        
        # 发起查询
        answers = resolver.resolve(domain, record_type)
        
        # 收集结果
        results = []
        for answer in answers:
            results.append(answer.to_text())
        
        return results
    except dns.resolver.NoAnswer:
        return f"No {record_type} record found for {domain}."
    except dns.resolver.NXDOMAIN:
        return f"Domain {domain} does not exist."
    except dns.exception.Timeout:
        return "DNS query timed out."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # domain = input("输入要查询的域名: ")
    # record_type = input("输入要查询的类型 (default A): ") or "A"
    # dns_server = input("指定DNS服务器 (default 114.114.114.114): ") or "114.114.114.114"
    # port = input("指定DNS服务器端口 (default 53): ") or "53"

    domain = "www.xxxx.com"
    record_type = "A"
    dns_server = "192.168.xx.xx"
    port = "xxx"    #蜜罐
    #port = "xxx"   #真实

    try:
        port = int(port)  # 将端口转为整数
    except ValueError:
        print("Invalid port number. Using default port 53.")
        port = 53

    results = query_dns(domain, record_type, dns_server, port)
    
    if isinstance(results, list):
        print(f"{record_type} records for {domain} (via {dns_server}:{port}):")
        for record in results:
            print(f"- {record}")
    else:
        print(results)