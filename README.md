# 🤖 Automação para Encerramento Comercial de Ordens de Manutenção (SAP)

## 📝 Descrição
Esta automação foi desenvolvida para rodar mensalmente com o objetivo de realizar o **encerramento comercial** de ordens de manutenção no sistema SAP que já foram encerradas tecnicamente (TECO) há mais de 90 dias. 

A solução visa reduzir o passivo de ordens abertas, garantindo a integridade dos dados financeiros e facilitando a gestão do backlog de manutenção.

Padrão - PE-3UTE-03159
GPI - CONFIRMAÇÃO E ENCERRAMENTO DE ORDENS NO SAP
Item 3.2.4 Encerramento comercial no sistema:

O encerramento comercial da ordem deve ser realizado somente 90 dias após o encerramento
técnico da mesma. Além disso, ele deve ocorrer somente após o encerramento de todos os
compromissos contábeis.

Status Inclusivo: ENTE (Encerrado Técnicamente)
Status Exclusivo: ENCE (Encerrado Comercialmente)

---

## ⚙️ Processo de Automação

O fluxo de trabalho segue as seguintes etapas:

1.  **Extração:** Identificação e extração de ordens com status de encerramento técnico (TECO) superior a 90 dias.
2.  **Armazenamento Inicial:** Geração de arquivo Excel (`.xlsx`) com a lista de ordens para conferência/auditoria.
3.  **Processamento:** Leitura do arquivo extraído e execução do script de encerramento no SAP.
4.  **Log de Execução:** Registro detalhado de cada ordem processada em um banco de dados **SQLite**.
5.  **Monitoramento:** Dashboard no **Power BI** conectado ao banco de dados para visualização de indicadores.

---

## 🛠️ Tecnologias e Frameworks

O projeto utiliza o ecossistema Python e ferramentas de BI:

| Ferramenta / Library | Descrição |
| :--- | :--- |
| **Python 3.x** | Linguagem base do projeto. |
| **Pandas** | Manipulação e limpeza dos dados de extração. |
| **SQLite** | Banco de Dados local para persistência e histórico de ordens. |
| **Openpyxl** | Interface para leitura e escrita de arquivos Excel. |
| **Psutil** | Monitoramento de processos do sistema (gestão do SAP GUI). |
| **Ipykernel** | Execução de scripts em ambiente interativo (Jupyter). |
| **Power BI** | Camada de visualização de dados e BI. |

---

## 🚀 Como Executar

### Pré-requisitos
* SAP GUI instalado e com **Scripting habilitado**.
* Python 3.8+ instalado.
* Acesso de escrita nas pastas do projeto.

### Instalação de Dependências
```bash
pip install pandas psutil openpyxl ipykernel