<template>
  <div>
    <nav class="bg-blue-500 p-4 shadow-lg fixed w-full z-10 top-0 left-0">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="text-white text-xl font-semibold">Titanic Survival Prediction</div>
        <div class="space-x-4">
          <router-link to="/" class="text-white hover:text-yellow-300">Home</router-link>
          <router-link to="/predict" class="text-white hover:text-yellow-300">Predict</router-link>
        </div>
      </div>
    </nav>
    <div class="container mx-auto px-4 py-16 pt-20"> <!-- Added pt-20 to create space below the fixed navbar -->
      <router-view />
    </div>
  </div>
</template>

<script>
export default {};
</script>
