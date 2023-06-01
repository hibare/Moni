<template>
    <q-card class="notifier-metric-card">
        <q-inner-loading showing v-if="notifierLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="calendar_month" size="xs" class="q-mr-xs" />Created
                on</div>
            <div class="q-mt-md card-title">{{ prettyDate(notifier?.created) }}</div>
        </q-card-section>
    </q-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { NotifierType } from '../../types';
import { useNotifierStore } from '../../store';
import { prettyDate } from '../../utils/utils';

const notifierStore = useNotifierStore()

const notifier = computed((): NotifierType => {
    return notifierStore.getNotifier as NotifierType
})

const notifierLoading = computed((): boolean => {
    return notifierStore.getNotifierLoading
})

</script>