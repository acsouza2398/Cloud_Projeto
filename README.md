# Projeto Cloud 2022.2
Ana Carolina Souza

## Pre-requisitos
Para uso do projeto, é preciso ter o Terraform e o AWS CLI instalados. <br>
Caso isso não seja o caso, é possível seguir o tutorial de instalação do Terraform [aqui](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) e o tutorial de instalação da AWS CLI [aqui](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). <br>
Além disso, é preciso ter uma conta root na AWS e acesso as credenciais dessa conta. Se não tiver uma conta, é possível criar uma [aqui](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) e ter aprender sobre as credenciais [aqui](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html).

## Instalação
Uma vez com os clis instalados e com a conta em mãos, é preciso configurar as credenciais da conta da AWS como variáveis de ambiente onde será executado o projeto. Para isso, abra um terminal e rode o comando `aws configure`. Isso irá dar 4 prompts para preencher com as seguintes informações:
<li> AWS Access Key ID
<li> AWS Secret Access Key
<li> Default region name
<li> Default output format <br>
  
Para mais informações sobre esses campos, acesse o site da AWS [aqui](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html). <br>
Uma vez configurada as credenciais da conta, é possível executar esse projeto.
  
## Uso do projeto
Crie uma pasta onde será rodado o programa principal. Uma vez criado, clone esse repositório com: <br>
  `git clone https://github.com/acsouza2398/Cloud_Projeto/` <br>
  
Para executar o projeto, entre na pasta clonada e rode `python main.py` em um terminal. O programa inicializa criando as pastas e arquivos de configuração iniciais e rodando `terraform init` para preparação do ambiente. Aguarde a finalização e o menu principal irá aparecer no terminal, mostrando quais são as escolhas possívels: criar, deletar e listar recursos ou fechar o programa. Todas as opções estão acompanhadas de instruções no terminal que aguardam respostas a serem digitadas no terminal. Para acessar alguma parte do programa, basta ir seguindo as instruções printadas no terminal. <br> <br>
Ao final de cada configuração de recursos, `terraform apply` é executado automaticamente, colocando em prática o que foi configurado na conta configurada anteriormente. Caso alguma configuração que o usuário digitou não seja compatível com o formato do terraform, como um CIDR block fora do padrão esperado, o erro do terraform irá ser mostrado no terminal. Nesse caso, o recurso não foi criado devido ao erro. Será necessário criá-lo novamente, mas com o erro corrigido de acordo com o apontado pela mensagem de erro. <br> <br>
O programa automaticamente cria as pastas e os arquivos usados com as configurações que o usuário escolheu. Enquanto o mesmo está executando, é possível abrí-los e visualizá-los, porém não é recomendado que estes sejam alterados para evitar erros ao rodar `terraform apply` novamente. <br> <br>
Ao final do programa, após fazer todas as alterações desejadas, basta fechar o programa pelo menu principal digitando 4. Isso irá fechar a sessão ao deletar todos os arquivos e pastas criadas, deixando o diretório limpo para o próximo uso.
  
## Mais informações
Para mais informações sobre o Terraform com AWS, acesse o site [aqui](https://developer.hashicorp.com/terraform/tutorials/aws-get-started), e sobre a AWS, acesse o site [aqui](https://aws.amazon.com/).
