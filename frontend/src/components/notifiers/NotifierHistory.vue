<template>
    <q-table title="History" :rows="rows" :columns="columns" :loading="historyLoading" row-key="timestamp"
        :fullscreen="fullscreen" @fullscreen="onFullscreen" v-model:pagination="pagination" class="q-px-sm q-py-sm">
        <template v-slot:top>
            <div class="col-12 card-title text-weight-medium"><q-icon name="history" size="xs" />
                History <q-btn icon="delete" size="sm" flat round color="red" class="float-right"
                    :disable="rows.length === 0" @click="toggleDeleteHistoryDialog" />
                <q-btn :icon="fullscreen ? 'fullscreen_exit' : 'fullscreen'" size="sm" flat round color="primary"
                    class="float-right" :disable="rows.length === 0" @click="toggleFullscreen" />
                <q-btn icon="refresh" size="sm" flat round color="primary" class="float-right"
                    :disable="rows.length === 0 || historyLoading" :loading="historyLoading" @click="refreshHistory" />
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
                <q-icon :name="props.row.status ? 'check' : 'close'" :color="props.row.status ? 'green' : 'red'"
                    size="1.2rem" />
            </q-td>
        </template>
        <template v-slot:body-cell-timestamp="props">
            <q-td :props="props">
                {{ prettyDate(props.row.timestamp) }}
            </q-td>
        </template>
    </q-table>

    <q-dialog v-model="deleteHistoryDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-red">Delete History?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to delete notifier history? This is a non-reversible operation.
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
import { HistoryType } from '../../types';
import { useNotifierHistoryStore } from '../../store';
import { prettyDate } from "../../utils/utils";

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

const notifierHistoryStore = useNotifierHistoryStore()

const rows = computed((): Array<HistoryType> => {
    return notifierHistoryStore.getHistory as HistoryType[]
})

const historyLoading = computed((): boolean => {
    return notifierHistoryStore.getHistoryLoading
})

const historyError = computed((): string => {
    return notifierHistoryStore.getHistoryError || ''
})

const historyDelLoading = computed((): boolean => {
    return notifierHistoryStore.getHistoryDelLoading
})

const toggleFullscreen = function () {
    fullscreen.value = !fullscreen.value
}

const toggleDeleteHistoryDialog = function () {
    deleteHistoryDialog.value = !deleteHistoryDialog.value
}

const deleteJobHistory = async function () {
    await notifierHistoryStore.deleteHistory(props.uuid)
    deleteHistoryDialog.value = false
}

const refreshHistory = () => {
    notifierHistoryStore.fetchHistory(props.uuid, true)
}

onMounted(() => {
    notifierHistoryStore.fetchHistory(props.uuid)
})
</script>
