<template>
<div class="main">
  <el-autocomplete
    popper-class="home-autocomplete"
    v-model="input_value"
    :fetch-suggestions="querySearch"
    placeholder="输入分类，如'人'"
    :trigger-on-focus="false"
    @select="handleSelect"
    @keyup.enter.native="handleChange">
    <template slot-scope="{ item }">
      <div class="nameZh">{{ item.nameZh }}</div>
      <span class="name">{{ item.name }}</span>
    </template>
  </el-autocomplete>
  <router-view />
</div>
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      input_value: '',
    }
  },
  mounted() {
    this.input_value = this.$route.query.hasOwnProperty('q')
      ? this.$route.query.q : ''
  },
  methods: {
    querySearch(queryString, cb) {
      this.$axios.get('/_autocomplete?q='+queryString)
      .then(res => {
        cb(res.data)
      })
      .catch(error => {
        console.log(error)
        cb([])
      })
    },
    handleSelect(item) {
      this.$router.push({
        path: `/${item.name}`
      })
    },
    handleChange(item) {
      this.$router.push({
        path: '/_search',
        query: {q: this.input_value}
      })
    }
  }
}
</script>
<style>
.home-autocomplete li {
  line-height: normal !important;
  padding: 7px 20px !important;
}
</style>
<style scoped>
.nameZh {
  text-overflow: ellipsis;
  overflow: hidden;
  font-size: 14px;
}
.name {
  font-size: 12px;
  color: #b4b4b4;
}
</style>
<style lang="scss" scoped>
.my-autocomplete {
  background: red;
}
.main {

}
.el-autocomplete {
  margin: 50px auto;
  margin-bottom: 20px;
  display: block;
  width: 70%;
  max-width: 600px;
}
</style>
