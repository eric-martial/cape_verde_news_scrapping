# Web Scraper de Notícias de Cabo Verde

Um scraper assíncrono para coletar notícias dos principais portais de notícias de Cabo Verde:
- A Nação (anacao.cv)
- Expresso das Ilhas (expressodasilhas.cv)
- Santiago Magazine (santiagomagazine.cv)

## Tecnologias Utilizadas

- Python 3.8+
- HTTPX para requisições HTTP assíncronas
- SQLite para armazenamento de dados
- Asyncio para processamento assíncrono
- Parsel para parsing HTML
- Loguru para logging

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
.
├── base_scraper.py       # Classe base para os scrapers
├── main.py              # Ponto de entrada da aplicação
├── scraper_logger.py    # Configuração de logging
├── storage_worker.py    # Gerenciamento de armazenamento
├── utils.py            # Funções utilitárias
└── scrapers/
    ├── anacao_scraper.py
    ├── expressodasilhas_scraper.py
    └── santiagomagazine_scraper.py
```

## Uso

Execute o scraper principal:
```bash
python -m main
```

## Funcionalidades

- Coleta assíncrona de notícias
- Rotação automática de User-Agents
- Sistema de proxy integrado
- Tratamento de rate limiting e retry
- Deduplicação de artigos
- Armazenamento em SQLite
- Logging extensivo

## Dados Coletados

Para cada artigo, são extraídos:
- Fonte (nome do portal)
- Título
- Autor
- Data de publicação
- Link
- Tópico/Categoria
- Conteúdo HTML

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

[Inserir informações de licença]

## Notas de Uso

- Respeite os robots.txt dos sites
- Configure delays apropriados entre requisições
- Monitore o uso de recursos do sistema
- Verifique regularmente a integridade do banco de dados