<template>
    <div>
        <q-card style="min-height: 145px;">
            <q-inner-loading showing v-if="notifierLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
            <template v-else-if="notifier">
                <q-item class="q-pb-none q-pt-md">
                    <q-item-section avatar class="q-pr-xs">
                        <q-avatar>
                            <q-icon :name="NotifierTypeMap[notifier.type].icon" size="23px"
                                :color="NotifierTypeMap[notifier.type].color" />
                        </q-avatar>
                    </q-item-section>
                    <q-item-section>
                        <div class="text-h6 q-pt-xs">{{ notifier?.title }}
                        </div>
                    </q-item-section>
                    <q-card-section class="flex flex-center q-pa-0 q-ma-0">
                        <div class="q-gutter-xs">
                            <q-btn flat round size="sm" icon="fa-solid fa-microscope" color="blue" @click="testNotifier"
                                :disable="notifierLoading || getNotifierTestLoading" :loading="getNotifierTestLoading">
                                <q-tooltip>Test Notifier</q-tooltip>
                            </q-btn>
                            <NotifierAddEdit :isEdit="true" />
                            <q-btn flat round size="sm" icon="delete" color="red"
                                @click="toggleNotifierDeleteDialog"><q-tooltip>Delete Notifier</q-tooltip>
                            </q-btn>
                        </div>
                    </q-card-section>
                </q-item>
                <q-card-section class="q-pt-sm">
                    <div class="fit text-caption q-pl-sm">{{ notifier?.description }}
                    </div>
                </q-card-section>
                <q-card-section class="q-pt-none">
                    <q-input filled dense readonly v-model="notifier.url" label="URL"
                        :type="urlVisibility ? 'text' : 'password'">
                        <template v-slot:append>
                            <q-icon :name="urlVisibility ? 'visibility_off' : 'visibility'" size="xs"
                                @click="toggleUrlVisibility" class="cursor-pointer q-pr-sm" />
                            <q-icon name="content_copy" size="xs" @click="copy2Clipboard(notifier.url)"
                                class="cursor-pointer" />
                        </template>
                    </q-input>
                </q-card-section>
            </template>
        </q-card>
    </div>

    <q-dialog v-model="notifierDeleteDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-primary">Delete Job?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to delete this notifier?. This is a non-reversible operation.
            </q-card-section>

            <q-card-actions align="right" class="q-pt-md">
                <q-btn flat label="Cancel" class="text-capitalize" v-close-popup />
                <q-btn flat label="Delete" class="text-capitalize" color="red" :loading="notifierStateLoading"
                    :disable="notifierStateLoading" @click="deleteNotifier" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useNotifierStore, useNotifiersStore } from '../../store';
import { NotificationType, NotifierType } from '../../types';
import { NotifierTypeMap, NotifyStatus } from '../../constants';
import { copy2Clipboard, showNotify } from "../../utils/utils"
import router from '../../router';
import NotifierAddEdit from './NotifierAddEdit.vue';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const notifierDeleteDialog = ref<boolean>(false)

const urlVisibility = ref<boolean>(false)

const notifierStore = useNotifierStore()

const notifier = computed((): NotifierType => {
    return notifierStore.getNotifier as NotifierType
})

const notifierLoading = computed((): boolean => {
    return notifierStore.getNotifierLoading
})

const toggleUrlVisibility = () => {
    urlVisibility.value = !urlVisibility.value
}

const getNotifierTestLoading = computed(() => {
    return notifierStore.getNotifierTestLoading
})

const testNotifier = async () => {
    const notification = {} as NotificationType

    const status = await notifierStore.testNotifier(props.uuid)
    if (status) {
        notification.status = NotifyStatus.Success
        notification.message = "Successfully Tested."
    } else {
        notification.status = NotifyStatus.Error
        notification.message = "Something went wrong."
    }
    showNotify(notification)
}

const notifierStateLoading = computed(() => {
    return notifierStore.getNotifierStateLoading
})

const toggleNotifierDeleteDialog = () => {
    notifierDeleteDialog.value = !notifierDeleteDialog.value
}

const deleteNotifier = async () => {
    const status = await notifierStore.deleteNotifier(props.uuid)
    if (status) {
        const notifiersStore = useNotifiersStore()
        notifiersStore.forceFetchNotifiers()
        router.push({ name: 'notifiers' })
    }
}

onMounted(() => {
    notifierStore.fetchNotifier(props.uuid)
})
</script>