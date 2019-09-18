<template>
<div class="main" v-if="myword!=null">
  <div class="name">{{myword.name}}</div>
  <div class="nameZh">{{myword.nameZh}}</div>
  <p class="descriptionZh">中文解释：
    {{myword.descriptionZh}}</p>
  <p class="description">英文解释：
    {{myword.description}}</p>
  <p v-if="myword.super!=''">父类：<router-link :to='myword.super.name'>
    {{myword.super.nameZh+' ('+myword.super.name+')'}}</router-link></p>
</div>
</template>
<script>
export default {
  name: 'word',
  data() {
    return {
      myword: null
    }
  },
  mounted() {
    this.$axios.get('/'+this.$route.params.word)
    .then(res => {
      this.myword = res.data
    })
    .catch(error => {
      console.log(error)
      this.myword = null
    })
  },
  methods: {
  }
}
</script>>
<style lang="scss" scoped>
.main {
  box-sizing: border-box;
  height: calc(100% - 150px);
  overflow: auto;
  padding: 20px;
}
.name {
  color: #919491;
  font-size: 14px;
  font-family: arial,tahoma,'Microsoft Yahei','\5b8b\4f53',sans-serif;
}
.nameZh {
  color: #333;
  font-size: 34px;
  font-family: arial,tahoma,'Microsoft Yahei','\5b8b\4f53',sans-serif;
}
p {
  font-size: 14px;
  word-wrap: break-word;
  color: #333;
  margin: 15px 0;
  text-indent: 1em;
  line-height: 24px;
  zoom: 1;
}
.description {}
</style>
