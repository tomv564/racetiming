<script>
  import { events } from './stores.js'

</script>

<ul>
  {#each $events as { type, state }, i }
    <li>{type}
  {/each}
</ul>

