<template>
    <q-table title="Notifiers" :rows="rows" :columns="columns" :loading="notifierJobsLoading" row-key="uuid"
        @row-click="onRowClicked" class="q-px-sm q-py-sm">
        <template v-slot:top>
            <div class="col-12 card-title text-weight-medium"><q-icon name="notifications" size="xs" />
                Jobs
            </div>
        </template>
        <template v-slot:loading>
            <q-inner-loading showing>
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
        </template>
        <template v-slot:no-data="{ icon, message }">
            <div class="full-width row flex-center text-accent q-gutter-sm">
                <span v-if="notifierJobsError">Something went wrong</span>
                <span v-else-if="!notifierJobsLoading">No Jobs found</span>
            </div>
        </template>

        <template v-slot:body-cell-title="props">
            <q-td :props="props">
                <q-avatar>
                    <q-icon name="cloud" size="18px" color="orange" v-if="props.row.favicon_url === null" />
                    <q-img height="20px" width="20px" spinner-color="black" spinner-size="0.8rem" fit="fill" v-else
                        :src="props.row.favicon_url">
                        <template v-slot:error>
                            <q-icon name="cloud" size="18px" color="orange" />
                        </template>
                    </q-img>
                </q-avatar>
                {{ props.row.title }}
            </q-td>
        </template>
        <template v-slot:body-cell-state="props">
            <q-td :props="props">
                <q-icon :name="props.row.state ? 'check' : 'close'" :color="props.row.state ? 'green' : 'red'"
                    size="1.2rem" />
            </q-td>
        </template>
        <template v-slot:body-cell-healthy="props">
            <q-td :props="props">
                <q-icon :name="props.row.healthy ? 'check' : 'close'" :color="props.row.healthy ? 'green' : 'red'"
                    size="1.2rem" />
            </q-td>
        </template>
    </q-table>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useNotifierJobsStore } from '../../store';
import { JobType, NotifierType } from '../../types';
import { QTableColumn } from 'quasar';
import router from '../../router';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const columns: QTableColumn[] = [

    {
        name: 'title',
        align: 'center',
        label: 'Title',
        field: 'title',
        sortable: true
    },
    {
        name: 'state',
        align: 'center',
        label: 'State',
        field: 'state',
        sortable: true
    },
    {
        name: 'healthy',
        align: 'center',
        label: 'Healthy',
        field: 'healthy',
        sortable: true
    },
]


const notifierJobStore = useNotifierJobsStore()

const rows = computed((): Array<JobType> => {
    return notifierJobStore.getJobs
})

const notifierJobsLoading = computed((): boolean => {
    return notifierJobStore.getJobsLoading
})

const notifierJobsError = computed((): string => {
    return notifierJobStore.getJobsError || ''
})

const onRowClicked = (event: Event, row: NotifierType, index: number) => {
    const uuid: string = row.uuid
    router.push({ name: 'jobDetails', params: { uuid } })
}

onMounted(() => {
    notifierJobStore.fetchNotifierJobs(props.uuid)
})
</script>
