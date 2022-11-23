import os
import json
import subprocess


#-------------------------Setup-------------------------#
print("Bem vindo ao Terraform CLI")
print("Inicializando os arquivos de configuração...")
subprocess.call(["mkdir", "terraform_files"], stdout=subprocess.DEVNULL)
os.chdir("terraform_files/")
subprocess.call(["mkdir", "east"], stdout=subprocess.DEVNULL)
subprocess.call(["mkdir", "west"], stdout=subprocess.DEVNULL)
print("Inicializando o Terraform...")
print("Aguarde...")
os.chdir("east/")
with open("config.tf", "w") as f:
    f.write('terraform {\n   required_providers {\n     aws = {\n  source  = "hashicorp/aws"\n       version = "~> 4.16"\n     }\n   }\n \n  required_version = ">= 1.2.0"\n  } \n')
    f.write('provider "aws" { \n region = "us-east-1" \n } \n')
    f.close()
subprocess.call(["terraform", "init", "-upgrade"], stdout=subprocess.DEVNULL)
os.chdir("../west/")
with open("config.tf", "w") as f:
    f.write('terraform {\n   required_providers {\n     aws = {\n  source  = "hashicorp/aws"\n       version = "~> 4.16"\n     }\n   }\n \n  required_version = ">= 1.2.0"\n  } \n')
    f.write('provider "aws" { \n region = "us-west-1" \n } \n')
    f.close()
subprocess.call(["terraform", "init", "-upgrade"], stdout=subprocess.DEVNULL)
os.chdir("..")
ins_name = []
ins_type = []
n = 0

#-------------------------Criar recursos-------------------------#
def criar(r):
    global n
    if r == "us-east-1":
        os.chdir("east/")
    else:
        os.chdir("west/")
    while(1):
        print("\nEscolha o que quer criar:")
        c = input("\nDigite 1 para VPC e sub-rede. \nDigite 2 para instâncias. \nDigite 3 para security group. \nDigite 4 para usuário no IAM. \nDigite 5 para voltar. \n")
        if c == "1":
            print("\nVPC \n")
            vpc_name = input("Escolha um nome para sua vpc (sem espaços): ")

            sn_name = input("Escolha um nome para sua sub-rede (sem espaços): ")

            print("Criando sua vpc e sub-rede...")
            print("Aguarde...")

            with open("network.tf", "w") as f:
                f.write('resource "aws_vpc" "' + vpc_name + '" { \n cidr_block = "10.0.0.0/16" \n enable_dns_support = "true" #gives you an internal domain name \n enable_dns_hostnames = "true" #gives you an internal host name \n instance_tenancy = "default" \n tags = { \n Name = "' + vpc_name + '" \n } \n } \n \n')
                f.write('resource "aws_subnet" "' + sn_name + '" {\n    vpc_id = "${aws_vpc.' + vpc_name + '.id}"\n    cidr_block = "10.0.1.0/24" \n    map_public_ip_on_launch = "true" //it makes this a public subnet\n    availability_zone = "' + r + 'a"\n    tags = {\n        Name = "' + sn_name + '"\n    }\n} \n \n')
                f.write('output "' + vpc_name + '_id" { \n     value = "${aws_vpc.' + vpc_name + '.id}" \n } \n  \n output "' + sn_name + '_id" { \n     value = "${aws_subnet.' + sn_name + '.id}" \n } \n\n')
                f.close()
            subprocess.call(["terraform", "apply", "-auto-approve"], stdout=subprocess.DEVNULL)

        elif c == "2":
            output,error = subprocess.Popen(["terraform", "state", "list"],stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
            output = output.decode("utf-8").split()
            all_ins = []
            for i in range(len(output)):
                if "aws_instance" in output[i]:
                    all_ins.append(output[i])
            if len(all_ins) > 0:
                n = len(all_ins)
            else:
                n = 0
                
            print("\nInstancia")
            ins_choice = 0
            if r == "us-east-1":
                ins_ami = "ami-0ee23bfc74a881de5"
            else:
                ins_ami = "ami-02d9763ac9c5603db"
            ins_name.append(input("\nEscolha um nome para sua instância: "))
            while(ins_choice != "1" or ins_choice != "2"):
                ins_choice = input("\nEscolha o tipo da sua instância: \n1 - t1.micro \n2 - t2.micro \n")
                if ins_choice == "1":
                    ins_type.append("t1.micro")
                    break
                elif ins_choice == "2":
                    ins_type.append("t2.micro")
                    break
                else:
                    print("\nOpção inválida. Tente novamente.\n")

            print("\nCriando sua instância...")
            print("Aguarde...")

            with open(ins_name[n] + "_ins.tf", "w") as f:
                f.write('resource "aws_instance" "' + ins_name[n] + '" {\n   ami           = "' + ins_ami + '" \n   instance_type = "' + ins_type[n] + '" \n   subnet_id = "${aws_subnet.' + sn_name + '.id}"\n \n   tags = {\n     Name = "' + ins_name[n] + '"\n   }\n }\n')
                f.write('output "' + ins_name[n] + '_id" { \n     value = "${aws_instance.' + ins_name[n] + '.id}" \n description = "Instance id de ' + ins_name[n] + '"\n } \n  \n')
                f.close()
            subprocess.call(["terraform", "apply", "-auto-approve"], stdout=subprocess.DEVNULL)                

        elif c == "3":
            print("\nSecurity Group \n")
            sg_name = input("Escolha um nome para seu security group: ")
            sg_ingress = []
            sg_ingress_fromport = []
            sg_ingress_toport = []
            sg_ingress_cidr = []
            sg_egress = []
            sg_egress_fromport = []
            sg_egress_toport = []
            sg_egress_cidr = []

            while(1):
                sg_rule = input("\nDigite 1 para criar uma regra ingress. \nDigite 2 para criar uma regra egress. \nDigite 3 para continuar. \n")
                if sg_rule == "1":
                    print("\nRegra ingress \n")
                    while(1):
                        prot = (input("Digite o protocolo (tcp, udp ou icmp): "))
                        if prot == "tcp" or prot == "udp" or prot == "icmp":
                            sg_ingress.append(prot)
                            break
                        else:
                            print("\nProtocolo inválido. Tente novamente.\n")
                    sg_ingress_fromport.append(input("Digite a porta de entrada: "))
                    sg_ingress_toport.append(input("Digite a porta de saída: "))
                    sg_ingress_cidr.append(input("Digite o CIDR: "))
                elif sg_rule == "2":
                    print("\nRegra egress \n")
                    while(1):
                        prot = (input("Digite o protocolo (tcp, udp ou icmp): "))
                        if prot == "tcp" or prot == "udp" or prot == "icmp":
                            sg_egress.append(prot)
                            break
                        else:
                            print("\nProtocolo inválido. Tente novamente.\n")
                    sg_egress_fromport.append(input("Digite a porta de entrada: "))
                    sg_egress_toport.append(input("Digite a porta de saída: "))
                    sg_egress_cidr.append(input("Digite o CIDR: "))
                elif sg_rule == "3":
                    break
                else:
                    print("\nOpção inválida. Tente novamente.\n")

            print("\nCriando seu security group...")
            print("Aguarde...")

            with open(sg_name + "_sg.tf", "w") as f:
                f.write('resource "aws_security_group" "' + sg_name + '" { \n vpc_id = "${aws_vpc.' + vpc_name + '.id}" \n tags = {\n     Name = "' + sg_name + '"\n   }\n } \n \n output "' + sg_name + '_id" { \n     value = "${aws_security_group.' + sg_name + '.id}" \n description = "Security Group id de ' + sg_name + '"\n  } \n ')
                for i in range(len(sg_egress)):
                    f.write('resource "aws_security_group_rule" "' + sg_name + '_egress' + i + '" { \n type              = egress { \n     from_port = ' + sg_egress_fromport[i] + ' \n     to_port = ' + sg_egress_toport[i] + ' \n     protocol = "' + sg_egress[i] + '" \n     cidr_blocks = ["' + sg_egress_cidr[i] + '"] \n security_group_id = aws_security_group.' + sg_name + '.id \n } \n' )
                for i in range(len(sg_ingress)):
                    f.write('resource "aws_security_group_rule" "' + sg_name + '_ingress' + i + '" { \n type = ingress { \n     from_port = ' + sg_ingress_fromport[i] + ' \n     to_port = ' + sg_ingress_toport[i] + ' \n     protocol = "' + sg_ingress[i] + '"\n     cidr_blocks = ["' + sg_ingress_cidr[i] + '"] \n security_group_id = aws_security_group.' + sg_name + '.id \n } \n')
                f.close()
            subprocess.call(["terraform", "apply", "-auto-approve"], stdout=subprocess.DEVNULL)

            while(1):
                ass_sg = input("\nDigite 1 para associar seu security group a uma instância. \nDigite 2 para concluir. \n")
                if ass_sg == "1":
                    output,error = subprocess.Popen(["terraform", "state", "list"],stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
                    output = output.decode("utf-8").split()
                    all_ins = []
                    for i in range(len(output)):
                        if "aws_instance" in output[i]:
                            all_ins.append(output[i])
                    if len(all_ins) == 0:
                        print("\nNão há instâncias criadas. \n")
                        break
                    else:
                        while(1):
                            if r == "us-east-1":
                                ins_ami = "ami-0ee23bfc74a881de5"
                            else:
                                ins_ami = "ami-02d9763ac9c5603db"
                            print("\nEscolha uma instância para associar seu security group: \n")
                            for i in range(len(all_ins)):
                                print(str(i) + " - " + all_ins[i])
                            ass_choice = int(input())
                            if ass_choice > len(all_ins):
                                print("\nOpção inválida. Tente novamente.\n")
                            else:
                                break
                        print("\nAssociando seu security group a instância escolhida...")
                        print("Aguarde...")

                        with open(ins_name[ass_choice] + "_ins.tf", "w") as f:
                            f.write('resource "aws_instance" "' + ins_name[ass_choice] + '" {\n   ami           = "' + ins_ami + '" \n   instance_type = "' + ins_type[ass_choice] + '" \n   subnet_id = "${aws_subnet.' + sn_name + '.id}" \n  vpc_security_group_ids = [aws_security_group.' + sg_name + '.id] \n \n   tags = {\n     Name = "' + ins_name[ass_choice] + '"\n   }\n }\n')
                            f.write('output "' + ins_name[ass_choice] + '_id" { \n     value = "${aws_instance.' + ins_name[ass_choice] + '.id}" \n description = "Instance id de ' + ins_name[ass_choice] + '"\n } \n  \n')
                            f.close()
                        subprocess.call(["terraform", "apply", "-auto-approve"], stdout=subprocess.DEVNULL)
                elif ass_sg == "2":
                    break
                else:
                    print("\nOpção inválida. Tente novamente.\n")

        elif c == "4":
            print("\nUsuario \n")
            usrname = input("Digite o nome do usuário (sem espaços): ")
            print("Criando usuário...")
            print("Aguarde...")

            with open(usrname + "_usr.tf", "w") as f:
                f.write('resource "aws_iam_user" "' + usrname + '"{ \n 	name = "' + usrname + '" \n tags = { \n    name = "' + usrname + '" \n  } \n } \n')
                f.write('resource "aws_iam_user_login_profile" "' + usrname + '_login_profile" { \n 	user = "${aws_iam_user.' + usrname + '.name}" \n 	password_reset_required = true \n 	password_length = 10 \n } \n')
                f.write('resource "aws_iam_access_key" "' + usrname + '_access_key" { \n	user = "${aws_iam_user.' + usrname + '.name}" \n} \n')
                f.close()
            subprocess.call(["terraform", "apply", "-auto-approve"], stdout=subprocess.DEVNULL)
            print("\nUsuário criado com sucesso. \n")
            print("As credenciais do usuário são: \n")
            subprocess.call(["terraform", "output", "-json", usrname])
            print("Anote a senha. Ela não será mostrada novamente. \n")
        elif c == "5":
            print("\nVoltar \n")
            break
        else:
            print("\nComando inválido \n")
    return

#-------------------------Deletar recursos-------------------------#
def deletar(r):
    if r == "us-east-1":
        os.chdir("east/")
    else:
        os.chdir("west/")
    while(1):
        del_choice = input("\nDigite 1 para deletar uma instância. \nDigite 2 para deletar um security group. \nDigite 3 para deletar um usuário. \nDigite 4 para deletar tudo. \nDigite 5 para voltar. \n")
        output,error = subprocess.Popen(["terraform", "state", "list"],stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
        output = output.decode("utf-8").split()
        if del_choice == "1":
            all_ins = []
            for i in range(len(output)):
                if "aws_instance" in output[i]:
                    all_ins.append(output[i])
            while(1):
                print("\nEscolha uma instância para deletar: \n")
                for i in range(len(all_ins)):
                    print(str(i) + " - " + all_ins[i])
                if len(all_ins) == 0:
                    print("\nNão há instâncias para deletar. \n")
                    break
                else:
                    delins_choice = int(input())
                    if delins_choice > len(all_ins):
                        print("\nOpção inválida. Tente novamente.\n")
                    else:
                        print("\nDeletando instância escolhida...")
                        print("Aguarde...")
                        subprocess.call(["terraform", "destroy", "--target", all_ins[delins_choice], "-auto-approve"], stdout=subprocess.DEVNULL)
                        break
        elif del_choice == "2":
            sgorrule_choice = input("\nDigite 1 para deletar um security group. \nDigite 2 para deletar um security group rule. \n")
            if sgorrule_choice == "1":
                all_sg = []
                for i in range(len(output)):
                    if "aws_security_group" in output[i]:
                        if "aws_security_group_rule" not in output[i]:
                            all_sg.append(output[i])
                while(1):
                    print("\nEscolha um security group para deletar: \n")
                    for i in range(len(all_sg)):
                        print(str(i) + " - " + all_sg[i])
                    if len(all_sg) == 0:
                        print("\nNão há security groups para deletar.\n")
                        break
                    else:
                        delsg_choice = int(input())
                        if delsg_choice > len(all_sg):
                            print("\nOpção inválida. Tente novamente.\n")
                        else:
                            print("\nDeletando security group escolhido...")
                            print("Aguarde...")
                            subprocess.call(["terraform", "destroy", "--target", all_sg[delsg_choice], "-auto-approve"], stdout=subprocess.DEVNULL)
                            break
            elif sgorrule_choice == "2":
                all_sgr = []
                for i in range(len(output)):
                    if "aws_security_group_rule" in output[i]:
                        all_sgr.append(output[i])
                while(1):
                    print("\nEscolha uma regra para deletar: \n")
                    for i in range(len(all_sg)):
                        print(str(i) + " - " + all_sgr[i])
                    if len(all_sgr) == 0:
                        print("\nNão há regras para deletar.\n")
                        break
                    else:
                        delsgr_choice = int(input())
                        if delsgr_choice > len(all_sgr):
                            print("\nOpção inválida. Tente novamente.\n")
                        else:
                            print("\nDeletando regra escolhida...")
                            print("Aguarde...")
                            subprocess.call(["terraform", "destroy", "--target", all_sgr[delsgr_choice], "-auto-approve"], stdout=subprocess.DEVNULL)
                            break
        elif del_choice == "3":
            all_usr = []
            for i in range(len(output)):
                if "aws_iam_user" in output[i]:
                    if "aws_iam_user_login_profile" not in output[i]:
                        all_usr.append(output[i])
            while(1):
                print("\nEscolha um usuário para deletar: \n")
                for i in range(len(all_usr)):
                    print(str(i) + " - " + all_usr[i])
                if len(all_usr) == 0:
                    print("\nNão há usuários para deletar. \n")
                    break
                else:
                    delusr_choice = int(input())
                    if delusr_choice > len(all_usr):
                        print("\nOpção inválida. Tente novamente.\n")
                    else:
                        print("\nDeletando usuário escolhido...")
                        print("Aguarde...")
                        subprocess.call(["terraform", "destroy", "--target", all_usr[delusr_choice], "-auto-approve"], stdout=subprocess.DEVNULL)
                        break
        elif del_choice == "4":
            print("\nDeletando tudo...")
            print("Aguarde...")
            subprocess.call(["terraform", "destroy", "-auto-approve"], stdout=subprocess.DEVNULL)
        elif del_choice == "5":
            print("\nVoltar \n")
            break
        else:
            print("\nComando inválido \n")
            

#-------------------------Listar recursos-------------------------#
def listar(r):
    if r == "us-east-1":
        os.chdir("east/")
    else:
        os.chdir("west/")
    while(1):
        list_choice = input("\nDigite 1 para listar tudo.\nDigite 2 para escolher ver apenas um recurso. \nDigite 3 para voltar. \n")
        if list_choice == "1":
            print("\nListando tudo...\n")
            subprocess.call(["terraform", "show"])
        elif list_choice == "2":
            print("\nListando todas as opções...\n")
            output,error = subprocess.Popen(["terraform", "state", "list"],stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
            output = output.decode("utf-8").split()
            for i in range(len(output)):
                if "aws_iam_user_login_profile" not in output[i]:
                    print(str(i) + " - " + output[i])
            if len(output) == 0:
                print("\nNão há nada para listar.\n")
            else:
                see_choice = input("\nDigite o número do recurso que deseja ver: \n")
                subprocess.call(["terraform", "state", "show", output[int(see_choice)]])
        elif list_choice == "3":
            print("\nVoltar \n")
            break
        else:
            print("\nComando inválido. \n")

#-------------------------Loop Principal-------------------------#
while(1):
    print("\nEscolha sua funcionalidade:")
    escolha = input("\nDigite 1 para criar algo. \nDigite 2 para deletar algo. \nDigite 3 para listar o que ja foi criado. \nDigite 4 para fechar o programa. \n")

    if escolha == "1":
        print("\nCriar \n")
        while(1):
            r = input('\nDigite 1 para região "us-east-1". \nDigite 2 para região "us-west-1". \n')
            if r == "1":
                criar("us-east-1")
                break
            elif r == "2":
                criar("us-west-1")
                break
            else:
                print("\nComando inválido. \n")
        os.chdir("..")
    elif escolha == "2":
        print("\nDeletar \n")
        while(1):
            r = input('\nDigite 1 para região "us-east-1". \nDigite 2 para região "us-west-1". \n')
            if r == "1":
                deletar("us-east-1")
                break
            elif r == "2":
                deletar("us-west-1")
                break
            else:
                print("\nComando inválido. \n")
        os.chdir("..")
    elif escolha == "3":
        print("\nListar \n")
        while(1):
            r = input('\nDigite 1 para região "us-east-1". \nDigite 2 para região "us-west-1". \n')
            if r == "1":
                listar("us-east-1")
                break
            elif r == "2":
                listar("us-west-1")
                break
            else:
                print("\nComando inválido. \n")
        os.chdir("..")
    elif escolha == "4":
        print("\nFechar \n")
        os.chdir("..")
        subprocess.call(["rm", "-r", "terraform_files"], stdout=subprocess.DEVNULL)
        break
    else:
        print("\nComando inválido \n")