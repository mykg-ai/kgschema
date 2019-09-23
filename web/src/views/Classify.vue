<template>
<div class="main">
  <el-tree :data="classes" :props="defaultProps" 
    @node-click="handleNodeClick">
    <span class="custom-tree-node" slot-scope="{ node, data }">
      <span>{{ node.label }}</span>
      <span>
        <el-button
         style="margin-left: 10px"
          type="text"
          size="mini"
          @click="buttonClick(node)">
          <font-awesome-icon :icon="['fas', 'external-link-alt']" />
        </el-button>
      </span>
    </span>
  </el-tree>
</div>
</template>
<script>
export default {
  name: 'classify',
  data() {
    return {
      defaultProps: {
        children: 'children',
        label: (data, node) => `${data.nameZh}(${data.name})`,
        name: (data, node) => data.name
      },
      classes: require('@/assets/classes.json')
    }
  },
  methods: {
    buttonClick(node) {
      var name = node.label.split('(')[1].split(')')[0]
      window.open('/'+name, '_blank')
    },
    handleNodeClick() {}
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
</style>
