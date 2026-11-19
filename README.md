# 🔷 Prisma

Um material, vários formatos acessíveis. O aluno ou professor envia uma apostila, slide, PDF ou foto da lousa e a IA devolve o mesmo conteúdo em:

- 🔊 **Áudio-descrição** (baixa visão e cegueira), com leitura em voz alta
- 📖 **Texto adaptado para dislexia** (frases curtas, espaçamento, contraste ajustável)
- ✅ **Micro-tarefas para TDAH** (checklist e progresso)
- 📚 **Glossário** em linguagem simples

> ⚠️ Conteúdo gerado por IA: o professor deve revisar antes de usar em sala (há um "Modo professor" para editar).
> Projeto de hackathon, ainda um protótipo. Não envie dados pessoais de alunos.

## Como rodar

1. Instale o [Python 3.10+](https://python.org) (no Windows, marque "Add python.exe to PATH").
2. Baixe este repositório e abra o terminal na pasta.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Pegue uma chave grátis em https://aistudio.google.com/app/apikey
5. Copie `.env.example` para `.env` e cole sua chave no lugar indicado.
6. Rode:
   ```bash
   streamlit run app.py
   ```
   O site abre em `http://localhost:8501`.

**Erros comuns:** `404` de modelo → troque `GEMINI_MODEL` no `.env` pelo nome de um modelo Flash atual (veja no AI Studio). `503` ou `429` → o Google está ocupado ou você atingiu o limite grátis; o app tenta de novo sozinho, espere um pouco.

## Onde mexer (para o time)

| Quero mudar... | Arquivo |
|---|---|
| Cores, fontes, contraste | `theme.py` |
| Cor dos botões | `.streamlit/config.toml` |
| O que a IA gera (tom, tamanho, regras) | `prompts.py` |
| Telas, abas, comportamento | `app.py` |

## Como contribuir

1. Crie uma *branch* (`git checkout -b minha-melhoria`).
2. Faça a mudança e teste rodando o app.
3. Abra um *Pull Request* explicando o que mudou.

**Nunca suba o arquivo `.env`** (ele já está no `.gitignore`).

## Ideias de próximos passos

Modo professor com salvar/compartilhar, suporte a mais idiomas, Libras, exportar em PDF/EPUB acessível, testes com alunos e AEE.

Licença: MIT.
