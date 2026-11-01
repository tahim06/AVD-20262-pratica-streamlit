# Justificativa das métricas — Dashboard 2

**Público-alvo do dashboard:** estudantes e profissionais de tecnologia que estão decidindo em qual setor e cidade procurar vaga. Todas as métricas respeitam os filtros da barra lateral (setor, cidade e intervalos) e mudam ao clicar em um setor no gráfico de salário mediano.

## Métrica 1: Vagas
- **Variável:** contagem de linhas do dataset (cada linha é uma vaga)
- **O que mede:** quantas vagas existem no recorte escolhido.
- **Por que foi escolhida:** antes de olhar salário, a pessoa precisa saber se existe oportunidade suficiente naquele setor/cidade. Também serve de referência para as outras métricas, porque uma porcentagem calculada em cima de 50 vagas pesa diferente de uma calculada em cima de 2.500.
- **Público-alvo:** quem está escolhendo onde procurar emprego.
- **Qual decisão pode ser apoiada por essa métrica?** Em quais setores ou cidades vale concentrar as candidaturas.
- **O que comunica ao público-alvo:** o tamanho do mercado no recorte ("aqui existem X vagas").

## Métrica 2: Salário mediano
- **Variável:** `salary_usd` (salário anual em dólar)
- **O que mede:** o salário do meio das vagas do recorte. Quando um setor é selecionado no gráfico, aparece também a variação em % em relação ao salário mediano de todos os setores filtrados.
- **Por que foi escolhida:** usei a mediana e não a média porque na EDA o salário não seguiu distribuição normal (Shapiro-Wilk rejeitou), e a mediana não é puxada por valores extremos. É a forma mais direta de responder "quanto paga".
- **Público-alvo:** quem está comparando setores pelo retorno financeiro.
- **Qual decisão pode ser apoiada por essa métrica?** Se compensa migrar ou se especializar em um setor específico.
- **O que comunica ao público-alvo:** "metade das vagas desse recorte paga até US$ X por ano".

## Métrica 3: Vagas remotas (%)
- **Variável:** `modalidade` (Remoto / Presencial, vinda de `remote_option`)
- **O que mede:** a proporção de vagas do recorte que aceitam trabalho remoto, com a variação em pontos percentuais quando um setor é selecionado.
- **Por que foi escolhida:** para quem mora no Brasil e olha vagas em cidades como Londres ou Singapura, ser remoto muda tudo. Na EDA vi que o remoto não muda o salário (Mann-Whitney não deu diferença), então a métrica que interessa é a disponibilidade, e não a diferença de pagamento.
- **Público-alvo:** quem não pode ou não quer se mudar de cidade.
- **Qual decisão pode ser apoiada por essa métrica?** Em quais setores e cidades dá para se candidatar sem precisar se mudar.
- **O que comunica ao público-alvo:** "X% das vagas aqui podem ser feitas de casa".

## Métrica 4: Vagas pagando US$ 200 mil ou mais (%)
- **Variável:** `salary_usd`
- **O que mede:** a proporção de vagas do recorte com salário anual a partir de US$ 200 mil, que é a faixa mais alta do dataset (vai até US$ 250 mil).
- **Por que foi escolhida:** a mediana mostra o centro, mas não mostra a chance de pegar uma vaga bem paga. Como a distribuição de salários é praticamente uniforme, essa proporção ajuda a ver se algum filtro concentra mais vagas no topo.
- **Público-alvo:** profissionais mais experientes, que já miram as vagas de maior salário.
- **Qual decisão pode ser apoiada por essa métrica?** Onde procurar se o objetivo é uma vaga na faixa mais alta.
- **O que comunica ao público-alvo:** "de cada 100 vagas desse recorte, X pagam US$ 200 mil ou mais".

## Visuais do Dashboard 2
1. **Salário mediano por setor (barras):** é o gráfico de controle. Clicar em uma barra filtra as métricas e os outros dois gráficos.
2. **Vagas por cidade e modalidade (barras empilhadas):** mostra onde estão as vagas e quanto de cada cidade é remoto.
3. **Vagas por faixa salarial e porte da empresa (barras agrupadas):** mostra se empresa grande paga mais que empresa pequena, uma pergunta que ficou em aberto na EDA.
