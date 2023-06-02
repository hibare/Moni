<template>
    <q-table title="Notifiers" :rows="rows" :columns="columns" :loading="notifierLoading" row-key="uuid"
        @row-click="onRowClicked" class="q-px-sm q-py-sm">
        <template v-slot:top>
            <div class="col-12 card-title text-weight-medium"><q-icon name="notifications" size="xs" />
                Noitifiers
            </div>
        </template>
        <template v-slot:loading>
            <q-inner-loading showing>
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
        </template>
        <template v-slot:no-data="{ icon, message }">
            <div class="full-width row flex-center text-accent q-gutter-sm">
                <span v-if="notifierError">Something went wrong</span>
                <span v-else-if="!notifierLoading">No notifiers found</span>
            </div>
        </template>
        <template v-slot:body-cell-type="props">
            <q-td :props="props">
                <q-icon :name="NotifierTypeMap[props.value].icon" :color="NotifierTypeMap[props.value].color" size="1.2rem">
                    <q-tooltip class="text-capitalize">
                        {{ props.value }}
                    </q-tooltip>
                </q-icon>
            </q-td>
        </template>
    </q-table>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { QTableColumn } from 'quasar';
import { useJobNotifiersStore } from '../../store';
import { NotifierType } from '../../types';
import { NotifierTypeMap } from '../../constants';
import router from '../../router';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const columns: QTableColumn[] = [
    {
        name: 'type',
        required: true,
        label: 'Type',
        align: 'left',
        field: 'type',
        sortable: true
    },
    {
        name: 'title',
        align: 'left',
        label: 'Title',
        field: 'title',
        sortable: true
    },
    {
        name: 'description',
        align: 'left',
        label: 'Description',
        field: 'description',
        sortable: true
    },
]

const rows = computed((): Array<NotifierType> => {
    const jobNotifiersStore = useJobNotifiersStore()
    return jobNotifiersStore.getNotifiers as NotifierType[]
})

const notifierLoading = computed((): boolean => {
    const jobNotifiersStore = useJobNotifiersStore()
    return jobNotifiersStore.getNotifiersLoading
})

const notifierError = computed((): string => {
    const jobNotifiersStore = useJobNotifiersStore()
    return jobNotifiersStore.getNotifiersError || ''
})

const onRowClicked = (event: Event, row: NotifierType, index: number) => {
    const uuid: string = row.uuid
    router.push({ name: 'notifierDetails', params: { uuid } })
}

onMounted(() => {
    const jobNotifierStore = useJobNotifiersStore()
    jobNotifierStore.fetchNotifiers(props.uuid)
})
</script>
