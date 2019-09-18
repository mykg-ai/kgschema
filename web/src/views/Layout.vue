<template>
<div class="main">
  <header :class="config.bannerClass">
    <div id="brand">
      <a>
        <!-- 
          https://fontawesome.com/icons/dharmachakra?style=solid
          https://fontawesome.com/icons/jedi?style=solid
          https://fontawesome.com/icons/cannabis?style=solid
          https://fontawesome.com/icons/dragon?style=solid
          https://fontawesome.com/icons/galactic-senate?style=brands
         -->
        <font-awesome-icon :icon="['fab', 'galactic-senate']" />
        <h1>kgSchema</h1>
        <p>中文知识图谱结构体</p>
      </a>
    </div>
    <div id="nav-bar">
      <nav>
        <ul>
          <router-link to="/"><li>首页</li></router-link>
          <router-link to="/_classify"><li>分类</li></router-link>
          <a href="https://github.com/mykg-ai/kgschema/wiki" target="_blank">
            <li>文档</li>
          </a>
        </ul>
      </nav>
      <div class="brand-a">
        <font-awesome-icon :icon="['fab', 'galactic-senate']" />
      </div>
    </div>
    <div id="nav-back"></div>
  </header>
  <!-- <nav>
    <router-link to="/" >首页</router-link>
    <router-link to="/_classify" >分类</router-link>
  </nav> -->
  <router-view />
  <footer>
    <div class="foot-container">
      <div>
        <span><router-link to="/_about">
          关于
        </router-link></span>
        <span><router-link to="/_link">
          友链
        </router-link></span>
        <!-- <span></span> -->
      </div>
      <div>
        <span>© 2019 <a>猫牙科技</a></span>
        <span>京ABC备32424234号</span>
      </div>
      <div class="media">
        <a href="https://github.com/mykg-ai/kgschema" target="_blank">
          <font-awesome-icon :icon="['fab', 'github']" />
        </a>
        <a href="https://www.linkedin.com/company/mykg-ai" target="_blank">
          <font-awesome-icon :icon="['fab', 'linkedin']" />
        </a>
        <a href="//chromit.mykg.ai" target="_blank">
          <font-awesome-icon :icon="['fab', 'weixin']" />
        </a>
        <a href="//chromit.mykg.ai" target="_blank">
          <font-awesome-icon :icon="['fas', 'paw']" />
        </a>
      </div>
    </div>
  </footer>
</div>
</template>
<script>
export default {
  name: 'layout',
  data() {
    return {
      config: {
        bannerClass: ''
      }
    }
  },
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
      var c = ''
      switch(route.name) {
        default:
          break
        case 'home':
          c = 'b-home'
          break
        case 'query':
        case 'word':
        case 'link':
        case 'classify':
        case 'about':
          c = 'b-search'
          break
      }
      this.config.bannerClass = c
    }
  }
}
</script>>
<style lang="scss" scoped>
.b-home {}
.b-search {
  // transform: translateY(-387px);
  #brand {
    display: none;
  }
  #nav-bar .brand-a {opacity: 1;}
}
// --- end theme ---

.main {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
header, footer {width: 100%;}
header {
  // background: rgba(4,42,43, 1);
  height: auto;
  background: url(./../assets/img/banner1.jpg) 50% 0 #483B6B;
  background-size: cover;
  &, a {
    font-size: 18px;
    color: #fff;
  }
  #brand {
    padding: 80px 0;
    text-align: center;
    svg {
      font-size: 120px;
      margin-bottom: 0px;
    }
    h1 {
      margin: 0 0 10px;
      font: 400 60px/1.2 FZZhengHeiM;
    }
    p {
      font: italic 25px/1 FZQingKeBenYueSongR;
      &::before, &::after {
        content: " - ";
      }
    }
  }
  #nav-bar {
    user-select: none;
    position: relative;
    nav {
      max-width: 700px;
      width: 50%;
      min-width: 400px;
      margin: 0 auto;
      ul a li {
        cursor: pointer;
        display: inline-block !important;
        height: 60px;
        display: block;
        padding: 0 1em;
        line-height: 62px;
        -webkit-transition: .15s ease-in-out;
        transition: .15s ease-in-out;
        border-bottom: 4px solid transparent;
        &:hover {
          border-bottom: 4px solid white;
        }
      }
    }
    .brand-a {
      position: absolute;
      width: 35px;
      height: 35px;
      top: 10px;
      font-size: 35px;
      left: 40px;
      opacity: 0;
      @media screen and (max-width: 512px) {
        display: none;
      }
    }
  }
  #nav-back {}
}
footer {
  position: absolute;
  background: #111;
  padding: 20px 0;
  bottom: 0;
  &, a {
    font-size: 12px;
    color: #666;
    user-select: none;
  }
  a:hover {
    color: #999;
  }
  .foot-container {
    @media screen and (max-width: 512px) {
      margin: 0 15px;
      width: auto;
    }
    @media screen and (min-width: 512px) and (max-width: 1024px) {
      margin: 0 20px;
      width: auto;
    }
    width: 960px;
    margin: 0 auto; 
    position: relative;
  }
  .foot-container > div {
    display: block;
    &:nth-child(2) {
      margin-top: 4px;
    }
    span:not(:first-child)::before {
      margin: 0 .3em;
      content: "\00B7";
    }
    &.media {
      position: absolute;
      top: 0; right: 0;
      @media screen and (max-width: 512px) {
        display: none;
      }
      a {
      font-size: 30px;
        svg {
          vertical-align: top !important;
        }
        &:not(:last-child) svg {
          margin-right: 10px;
        }
      }
    }
  }
}

</style>
