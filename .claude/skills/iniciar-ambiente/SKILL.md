---
name: iniciar-ambiente
description: >
  Prepara a máquina para o cérebro funcionar: confere o git, confirma que o Credential
  Manager (que vem junto com o Git for Windows) está ativo, e configura a identidade do
  git. Chamada pelo /iniciar no passo 2, mas pode ser usada sozinha quando a pessoa troca
  de máquina ou quando o envio para de funcionar.
  Triggers: "/iniciar-ambiente", "conecta meu github", "o push parou de funcionar".
disable-model-invocation: true
---

# Adaptador de runtime

@../../../skills/inicio/iniciar-ambiente/SKILL.md
