<template>
    <q-table title="History" :rows="rows" :columns="columns" :loading="historyLoading" row-key="timestamp"
        :fullscreen="fullscreen" @fullscreen="onFullscreen" v-model:pagination="pagination" class="q-px-sm q-py-sm">
        <template v-slot:top>
            <div class="col-12 card-title text-weight-medium"><q-icon name="history" size="xs" />
                History <q-btn icon="delete" size="sm" flat round color="red" class="float-right"
                    :disable="rows.length === 0" @click="toggleDeleteHistoryDialog" />
                <q-btn :icon="fullscreen ? 'fullscreen_exit' : 'fullscreen'" size="sm" flat round color="primary"
                    class="float-right" :disable="rows.length === 0" @click="toggleFullscreen" />
            </div>
        </template>
        <template v-slot:loading>
            <q-inner-loading showing>
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
        </template>
        <template v-slot:no-data="{ icon, message }">
            <div class="full-width row flex-center text-accent q-gutter-sm">
                <span v-if="historyError">Something went wrong</span>
                <span v-else-if="!historyLoading">No history found</span>
            </div>
        </template>
        <template v-slot:body-cell-success="props">
            <q-td :props="props">
                <q-icon :name="props.row.success ? 'check' : 'close'" :color="props.row.success ? 'green' : 'red'"
                    size="1.2rem" />
            </q-td>
        </template>
    </q-table>

    <q-dialog v-model="deleteHistoryDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-red">Delete History?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to delete job history? This is a non-reversible operation.
            </q-card-section>

            <q-card-actions align="right" class="q-pt-md">
                <q-btn flat label="Cancel" class="text-capitalize" color="primary" v-close-popup />
                <q-btn flat label="Delete" class="text-capitalize" color="red" :loading="historyDelLoading"
                    @click="deleteJobHistory" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { QTableColumn } from 'quasar';
import { useJobHistoryStore } from '../../store/jobHistory';
import { HistoryType } from '../../types';

const fullscreen = ref<boolean>(false)
const pagination = ref<Record<string, any>>({
    rowsPerPage: 5
})
const deleteHistoryDialog = ref<boolean>(false)

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const columns: QTableColumn[] = [
    {
        name: 'timestamp',
        required: true,
        label: 'Timestamp',
        align: 'left',
        field: 'timestamp',
        sortable: true
    },
    {
        name: 'status_code',
        align: 'left',
        label: 'Status Code',
        field: 'status_code',
        sortable: true
    },
    {
        name: 'success',
        align: 'left',
        label: 'Success',
        field: 'success',
        sortable: true
    },
    {
        name: 'error',
        align: 'left',
        label: 'Error',
        field: 'error',
        sortable: true
    },
]

const onFullscreen = (val: boolean) => {
    pagination.value.rowsPerPage = val ? 10 : 5
}

const rows = computed((): Array<HistoryType> => {
    const jobHistoryStore = useJobHistoryStore()
    return jobHistoryStore.getHistory as HistoryType[]
})

const historyLoading = computed((): boolean => {
    const jobHistoryStore = useJobHistoryStore()
    return jobHistoryStore.getHistoryLoading
})

const historyError = computed((): string => {
    const jobHistoryStore = useJobHistoryStore()
    return jobHistoryStore.getHistoryError || ''
})

const historyDelLoading = computed((): boolean => {
    const jobHistoryStore = useJobHistoryStore()
    return jobHistoryStore.getHistoryDelLoading
})

const toggleFullscreen = function () {
    fullscreen.value = !fullscreen.value
}

const toggleDeleteHistoryDialog = function () {
    deleteHistoryDialog.value = !deleteHistoryDialog.value
}

const deleteJobHistory = async function () {
    const jobHistoryStore = useJobHistoryStore()
    await jobHistoryStore.deleteHistory(props.uuid)
    deleteHistoryDialog.value = false
}

onMounted(() => {
    const jobNotifierStore = useJobHistoryStore()
    jobNotifierStore.fetchHistory(props.uuid)
})
</script>
