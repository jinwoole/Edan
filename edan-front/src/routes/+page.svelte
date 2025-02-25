<script>
  import ChatBox from '$lib/components/ChatBox.svelte';
</script>

<main>
  <header>
    <h1>에단</h1>
    <p>Chat with a VLLM-powered AI model</p>
  </header>
  
  <section class="chat-container">
    <ChatBox />
  </section>
</main>

<style>
  main {
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  
</style>
