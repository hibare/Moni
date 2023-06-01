<template>
    <q-page container class="q-pa-md q-col-gutter-md">
        <error :text="notiferError" v-if="notiferError"></error>

        <template v-else>
            <NotifierDetails :uuid="(uuid as string)" v-if="uuid !== null"></NotifierDetails>

            <div class="row q-col-gutter-md q-col-gutter-y-md">
                <div class="col-md-3 col-12">
                    <NotifierCreated />
                </div>
                <div class="col-md-3 col-12">
                    <NotifierUpdated />
                </div>
                <div class="col-md-3 col-12">
                    <NotifierDelivery :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
                <div class="col-md-3 col-12">
                    <NotifierJobsCount :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
            </div>

            <div class="row q-col-gutter-md q-col-gutter-y-md">
                <div class="col-md-6 col-12">
                    <NotifierJobs :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
                <div class="col-md-6 col-12">
                    <NotifierHistory :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
            </div>
        </template>
    </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import router from '../../router';
import { useNotifierStore } from '../../store';
import Error from '../../components/Error.vue';
import NotifierDetails from "../../components/notifiers/NotifierDetails.vue"
import NotifierCreated from '../../components/notifiers/NotifierCreated.vue';
import NotifierUpdated from '../../components/notifiers/NotifierUpdated.vue'
import NotifierDelivery from '../../components/notifiers/NotifierDelivery.vue';
import NotifierJobsCount from '../../components/notifiers/NotifierJobsCount.vue';
import NotifierJobs from '../../components/notifiers/NotifierJobs.vue';
import NotifierHistory from '../../components/notifiers/NotifierHistory.vue';

const uuid = ref<String | null>(null)

const notiferError = computed((): string => {
    const notifierStore = useNotifierStore()
    return notifierStore.getNotifierError || ''
})

onMounted(() => {
    uuid.value = router.currentRoute.value.params.uuid as string
})

</script>
