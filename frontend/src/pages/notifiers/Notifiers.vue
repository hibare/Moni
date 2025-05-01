<template>
    <q-page container class="q-pb-xl">
        <div class="q-pa-md q-gutter-md" v-if="!notifierError">
            <div class="row">
                <q-input filled dense v-model="search" label="Search..." style="width: calc(100% - 100px)"
                    :disable="!notifiers.length">
                    <template v-slot:prepend>
                        <q-icon name="search" />
                    </template>
                    <template v-slot:append>
                        <q-icon name="clear" size="xs" class="cursor-pointer" @click="clearSearch" v-if="search" />
                    </template>
                </q-input>
                <q-btn round flat icon="refresh" @click="refreshNotifiers"
                    :disable="notifierLoading || notifiers.length === 0">
                    <q-tooltip>
                        Click to refresh
                    </q-tooltip>
                </q-btn>
                <NotifierAddEdit iconSize="md" />
            </div>
        </div>

        <div class="row absolute-center" v-if="!notifiers.length && !notifierLoading && !notifierError">
            <div class="text-subtitle2"><q-icon name="psychology_alt" size="sm" /> No Notifiers found<br />
                Click
                <NotifierAddEdit iconSize="sm" /> to add a Notifier.
            </div>
        </div>

        <div class="q-mx-md q-mt-sm ">
            <q-inner-loading :showing="notifierLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>

            <error :text="notifierError" v-if="notifierError"></error>

            <div class="row q-col-gutter-md q-col-gutter-y-lg" v-else>
                <div class="col-md-3 col-12 clickable-card " v-for="notifier in filteredNotifiers"
                    @click="route2Details(notifier.uuid)">
                    <q-card style="min-height: 70px">
                        <q-item>
                            <q-item-section avatar class="q-pr-xs">
                                <q-avatar>
                                    <q-icon :name="NotifierTypeMap[notifier.type].icon" size="20px"
                                        :color="NotifierTypeMap[notifier.type].color" />
                                </q-avatar>
                            </q-item-section>

                            <q-item-section>
                                <q-item-label>
                                    <div class="text-h6 q-pt-sm">{{ notifier.title }}</div>
                                </q-item-label>
                            </q-item-section>
                        </q-item>
                    </q-card>
                </div>
            </div>
        </div>

    </q-page>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useNotifiersStore } from '../../store';
import router from '../../router';
import { NotifierTypeMap } from '../../constants';
import Error from '../../components/Error.vue';
import NotifierAddEdit from '../../components/notifiers/NotifierAddEdit.vue';

const search = ref<string>('')

const notifiersStore = useNotifiersStore()

const clearSearch = () => {
    search.value = ''
}

const notifiers = computed(() => {
    return notifiersStore.getNotifiers
})

const notifierLoading = computed(() => {
    return notifiersStore.getNotifiersLoading
})

const notifierError = computed(() => {
    return notifiersStore.getNotifiersError
})

const filteredNotifiers = computed(() => {
    const searchStr = search.value.toLowerCase().trim()

    if (!searchStr)
        return notifiers.value

    return notifiers.value.filter(notifier => {
        return (notifier.type.toLowerCase().includes(searchStr) || notifier.title.toLowerCase().includes(searchStr) || notifier.description.toLowerCase().includes(searchStr))
    })
})

const refreshNotifiers = () => {
    notifiersStore.forceFetchNotifiers()
}

const route2Details = (uuid: string) => {
    router.push({ name: 'notifierDetails', params: { uuid } })
}

onMounted(() => {
    notifiersStore.fetchNotifiers()
})
</script>
