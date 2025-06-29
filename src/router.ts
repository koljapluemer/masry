import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import EditUnitOfMeaning from './views/unitOfMeaning/EditUnitOfMeaning.vue'
import ListUnitOfMeanings from './views/unitOfMeaning/ListUnitOfMeanings.vue'
import ManageLanguages from './views/language/ManageLanguages.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/unit-of-meaning/add/:id?',
    name: 'AddUnitOfMeaning',
    component: EditUnitOfMeaning
  },
  {
    path: '/unit-of-meaning/list',
    name: 'ListUnitOfMeanings',
    component: ListUnitOfMeanings
  },
  {
    path: '/languages',
    name: 'ManageLanguages',
    component: ManageLanguages
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
