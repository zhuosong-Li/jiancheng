<template>
    <div ref="mermaidChart" class="mermaid">
      {{ chartDefinition }}
    </div>
  </template>
  
  <script>
  import mermaid from 'mermaid';
  
  export default {
    props: {
      chartDefinition: {
        type: String,
        required: true,
      },
    },
    mounted() {
      mermaid.initialize({
        startOnLoad: true,
        theme: 'forest',
        flowchart: {
          useMaxWidth: true,
          htmlLabels: true,
        },
        fontSize: 10,
        securityLevel: 'loose'
        
        
      });
      mermaid.contentLoaded();
    },
  };
  </script>
  
  <style scoped>
  .mermaid {
    max-width: 100%;
    overflow-x: auto;
    height: 800px;
    
  }
  </style>
  