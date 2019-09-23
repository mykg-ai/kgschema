<template>
<div class="main" v-loading="searchLoading">
  <div>
    <div class="word" v-for="word in words">
      <div class="title">
        <router-link :to="'/'+word.name">
          {{word.nameZh}} · {{word.name}}
        </router-link>
      </div>
      <div class="descriptionZh">{{word.descriptionZh}}</div>
      <div class="description">{{word.description}}</div>
    </div>
  </div>
  
  <div v-show="!searchLoading&&words.length==0" style="text-align: center">
    Ops! 没有相关内容...
  </div>
</div>
</template>

<script>

export default {
  name: 'search',
  data() {
    return {
      words: [],
      is_loading: true
    }
  },
  props: ['searchLoading'],
  watch: {
    $route(_new, _old) {
      this.changeRoute(_new)
    }
  },
  mounted() {
    this.changeRoute(this.$route)
  },
  methods: {
    changeRoute(route) {
      var sug = document.querySelector('.el-autocomplete-suggestion')
      sug.style.display = 'none'
      this.$axios.get('_search?q='+route.query.q)
      .then(res => {
        this.words = res.data
      })
      .catch(error => {
        console.log(error)
        this.words = []
      })
      .then(() => {
        // this.searchLoading = false
        console.log(9999)
        this.$parent.changeSearchLoading()
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.main {
  height: calc(100% - 300px);
  overflow: auto;
}
.word {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 70%;
  max-width: 900px;
  margin: 20px auto;
  // margin-top: 0;
  padding-bottom: 20px;
  padding-top: 10px;
  &:first-child { padding-top: 0px; margin-top: 10px; }
  &:not(:last-child)::after {
    position: absolute;
    bottom: -1px;
    width: calc(80% + 60px);
    max-width: 900px;
    content: "";
    border-bottom: 2px solid #DDD;
  }
  .title {
    font-size: 20px;
    font-weight: 400;
    a:hover {
      cursor: pointer;
      color: #00BCD4;
      transition: color .2s;
    }
  }
  .descriptionZh {
    color: #666;
    padding: 5px 0px;
  }
  .description {
    color: #999;
  }
}
</style>