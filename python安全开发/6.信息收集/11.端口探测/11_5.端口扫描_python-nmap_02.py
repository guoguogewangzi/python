import nmap 

nm = nmap.PortScanner()
nm.scan('www.baidu.com','80,443')
host_list=nm.all_hosts()
for host in host_list:
    print(host + '/' + nm[host].hostname() + '-----' + nm[host].state() + '/' + ''.join(nm[host].all_protocols()))
    port_list=nm[host].all_tcp()
    for i in port_list:
        port_info = nm[host].tcp(i)
        print(f'[+]{i}/'+ port_info['state'] + '\t',end='')
        if port_info['product'] == '':
            print('service: Unknown')
        else:
            print('server:' + port_info['product'])