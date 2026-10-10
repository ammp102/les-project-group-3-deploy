# AGENTS.md

> **Governança de Engenharia e Diretrizes de Desenvolvimento com IA**  
> **Contexto:** MESW — Laboratório de Engenharia de Software (2026/27)  
> **Produto:** Patas — Plataforma Colaborativa de Proteção Animal

---

## 1. Princípios de Relação Humano-Agente & Decisões

* **Decisões de Arquitetura Pertencem ao Desenvolvedor:**
  * O agente **não toma decisões de arquitetura de forma autónoma**.
  * O agente pode sugerir alternativas arquiteturais, devendo explicitar trade-offs claros (acoplamento, coesão, testabilidade, manutenibilidade) e aguardar aprovação explícita antes de avançar.
* **Obrigatoriedade de Explicação Didática ("The Room Wins"):**
  * Qualquer membro da equipa pode ser chamado para defender o código individualmente na avaliação presencial.
  * Todo o código gerado pelo agente deve ser explicado de forma clara ao desenvolvedor (exceto alterações mecânicas triviais). Se a equipa não compreender o código gerado, esse código não entra no repositório.
* **Rastreabilidade e AI Log:**
  * O uso de IA deve ser auditável e documentado.
  * Qualquer alucinação, proposta incorreta ou falha do agente que exija intervenção e correção humana deve ser sinalizada para registo no `CLAIM.md` da respetiva iteração.

---

## 2. Paradigma de Modelação & Padrões de Desenho

* **Orientação a Objetos Obrigatória:**
  * Todo o desenho do sistema deve seguir princípios estritos de Orientação a Objetos (OOP).
  * Encapsulamento de estado, polimorfismo, separação clara de responsabilidades (SRP) e modelos ricos de domínio.
  * Proibido o uso de modelos anémicos com lógica procedural dispersa em serviços quando o domínio deve encapsular os seus próprios invariantes.
* **Aplicação Deliberada de Design Patterns:**
  * Usar padrões clássicos (GoF) sempre que houver justificação funcional concreta:
    * **Strategy:** Para algoritmos intercambiáveis de cálculo de afinidade no *Matchmaker* e políticas de triagem.
    * **Factory / Abstract Factory:** Para instanciação controlada de agregados complexos e tipos de acolhimento.
    * **State:** Para máquinas de estados finitos formais do ciclo de vida do animal e do *Adoption Tracker*.
    * **Observer:** Para eventos de domínio e notificações desacopladas perante transições de estado.
  * Proibido o *overengineering*: cada padrão introduzido deve resolver um problema concreto de extensibilidade ou acoplamento.

---

## 3. Estratégia de Testes Focada em Especificações

* **Specification-Driven Testing:**
  * Os testes devem verificar contratos de especificação, invariantes de domínio e regras de negócio concretas.
  * Proibido criar testes inflacionados apenas para aumentar contagens brutas ou métricas vazias de cobertura.
* **Capacidade de Falha Real:**
  * Todo o teste deve ser capaz de quebrar perante uma regressão real do comportamento esperado. Evitar testes assentes exclusivamente em mocks da implementação interna.
* **Fatias Verticais Funcionais (Vertical Slices):**
  * O código e os testes devem validar fatias verticais que executam da entrada do utilizador até à camada de persistência.

---

## 4. Qualidade, Ferramentas e Linters

* **Conformidade Obrigatória com Linters e Formatadores:**
  * Todo o código deve passar nos linters e ferramentas estáticas configuradas no projeto sem avisos (*warnings*) pendentes.
  * Proibido suprimir regras de análise estática sem justificação técnica fundamentada.
* **Automação e Integração Contínua (CI):**
  * A suíte de testes de especificação e os linters devem passar a 100% no pipeline de CI antes de qualquer merge.

---

## 5. Regras Proibidas (Red Lines)

1. **Dead Demos:** Proibido desenvolver interfaces isoladas ou maquetes visuais suportadas por dados estáticos sem ligação à lógica e ao modelo de dados.
2. **Friday Dumps:** Proibido acumular alterações massivas sem histórico incremental de commits. O histórico de versões deve refletir progresso distribuído no tempo.
3. **Código Opaco / Não Explicado:** Código cuja razão de existir ou funcionamento não seja dominado pelo desenvolvedor não pode ser submetido.
4. **Violação da Definition of Done:** Nenhuma funcionalidade é dada como concluída se não puder ser executada na tag da respetiva iteração (`iter-N`).