---
name: iniciar-repo
description: >
  Cria o repositório pessoal da pessoa a partir do template, coloca a pasta no layout
  ~/bravo/, clona o inbox da alçada dela ao lado, e preenche o .cerebro.yml com os
  endereços. Chamada pelo /iniciar no passo 3. Depende do iniciar-ambiente.
  Triggers: "/iniciar-repo", "cria meu repositório".
disable-model-invocation: true
---

# Adaptador de runtime

@../../../skills/inicio/iniciar-repo/SKILL.md
