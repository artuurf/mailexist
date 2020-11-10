import dns.resolver
import socket
import smtplib

archivelist = open('/home/artursantos/Downloads/mails1.txt', 'r')

for addressToVerify in archivelist:
    addressToVerify = addressToVerify.rstrip('\n')
    print(addressToVerify)
    domain = addressToVerify.split('@')

    try:
        records = dns.resolver.resolve(domain[1], 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation

        server.connect(mxRecord)
        server.helo(host)

        server.mail('me@domain.com')
        code, message = server.rcpt(str(addressToVerify))
        server.quit()

        arquivo = open("/home/artursantos/Downloads/lista_contas2.txt", "a")

        # Assume 250 as Success
        if code == 250:
            print('Existente')
            arquivo.writelines(f'{addressToVerify};Existente\n')
            arquivo.close()
        else:
            print('Conta não existe!')
            arquivo.writelines(f'{addressToVerify};Não existe\n')
            arquivo.close()

    except:
        pass

archivelist.close()
