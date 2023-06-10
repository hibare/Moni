<template>
    <q-btn round flat :icon="isEdit ? 'edit' : 'add'" :size="iconSize" color="primary" @click="openDialog">
        <q-tooltip>
            Click to add a Notifier
        </q-tooltip>
    </q-btn>
    <q-dialog v-model="notifierAddEditDialog" class="q-pa-md" persistent>
        <q-card class="q-px-md q-pt-sm" style="width: 800px; max-width: 80vw;">
            <q-inner-loading showing v-if="notifierLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
            <q-card-section>
                <div class="text-h6">{{ getDialogHeader }}</div>
            </q-card-section>
            <q-card-section>
                <q-form ref="addEditNotifierForm">
                    <q-select filled v-model="notifierItem.type" :options="notifierTypeOptions" emit-value label="Type"
                        :readonly="props.isEdit" lazy-rules :rules="rules.emptyRule"
                        @update:model-value="notifierItemOnChange">
                        <template v-slot:selected>
                            <span class="q-ml-xs q-mr-xs text-capitalize" v-if="notifierItem.type">
                                <q-icon :color="NotifierTypeMap[notifierItem.type].color" text-color="white"
                                    :name="NotifierTypeMap[notifierItem.type].icon" />
                                {{ notifierItem.type }}
                            </span>
                        </template>
                        <template v-slot:option="scope">
                            <q-item v-bind="scope.itemProps">
                                <q-item-section avatar>
                                    <q-icon :name="NotifierTypeMap[scope.opt.value].icon"
                                        :color="NotifierTypeMap[scope.opt.value].color" size="1.2rem" />
                                </q-item-section>
                                <q-item-section>
                                    <q-item-label class="text-capitalize">{{ scope.opt.label }}</q-item-label>
                                </q-item-section>
                            </q-item>
                        </template>
                    </q-select>
                    <q-input dense filled v-model="notifierItem.title" label="Title" lazy-rules :rules="rules.titleRule" />
                    <q-input filled dense v-model="notifierItem.url" label="URL" :type="urlVisibility ? 'text' : 'password'"
                        lazy-rules :rules="NotifierTypeMap[notifierItem.type].rule" v-if="notifierItem.type"
                        @update:model-value="notifierItemOnChange">
                        <template v-slot:append>
                            <q-icon :name="urlVisibility ? 'visibility_off' : 'visibility'" size="xs"
                                @click="toggleUrlVisibility" class="cursor-pointer" />
                        </template>
                    </q-input>
                    <q-input dense v-model="notifierItem.description" label="Description" filled autogrow />
                </q-form>
            </q-card-section>
            <q-card-section align="right">
                <q-btn flat label="Cancel" class="text-capitalize" @click="closeDialog" />
                <q-btn flat color="primary" label="Submit" @click="submitNotifier" class="text-capitalize"
                    :disable="notifierLoading" v-if="notifierItem.valid" />
                <q-btn flat color="primary" label="Test" @click="testNotifier" class="text-capitalize"
                    :disable="testBareNotifierLoading" :loading="testBareNotifierLoading" v-else />
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { NotifierTypeMap, NotifyStatus } from "../../constants"
import { useNotifierHistoryStore, useNotifierJobsStore, useNotifierStore, useNotifiersStore } from '../../store';
import { NotifierAddEditType, NotificationType } from '../../types'
import rules from '../../utils/rules'
import notifiersApi from "../../api/notifiers";
import { getErrorMessage, showNotify } from '../../utils/utils';

const props = defineProps({
    iconSize: {
        type: String,
        default: "sm"
    },
    isEdit: {
        type: Boolean,
        required: false
    }
})

const addEditNotifierForm = ref(null)
const notifierAddEditDialog = ref<boolean>(false)
const urlVisibility = ref<boolean>(false)
const notifierItem = ref<NotifierAddEditType>({
    title: "",
    description: "",
    url: "",
    type: "",
    valid: false,
})
const notifierDefaultItem: NotifierAddEditType = {
    title: "",
    description: "",
    url: "",
    type: "",
    valid: false,
}
const testBareNotifierLoading = ref<boolean>(false)

const notifierStore = useNotifierStore()

const getDialogHeader = computed((): string => {
    return props.isEdit ? "Edit Notifier" : "Add Notifier"
})

const openDialog = () => {
    notifierAddEditDialog.value = true
}

const closeDialog = () => {
    notifierAddEditDialog.value = false
}

const toggleUrlVisibility = () => {
    urlVisibility.value = !urlVisibility.value
}

const notifierLoading = computed(() => {
    return notifierStore.getNotifierLoading
})

const notifierTypeOptions = computed(() => {
    return Object.entries(NotifierTypeMap).map(([key, _]) => ({
        label: key,
        value: key
    }));
})

const notifierItemOnChange = () => {
    notifierItem.value.valid = false
}


const submitNotifier = () => {
    // @ts-ignore
    addEditNotifierForm.value?.validate().then(async (success: Boolean) => {
        if (success) {
            props.isEdit ? editNotifier() : addNotifier()
        }
    })
}

const addNotifier = async () => {
    const notification = {} as NotificationType
    const notifierStore = useNotifierStore()
    const status = await notifierStore.addNotifier(notifierItem.value)

    if (status) {
        closeDialog()

        notification.status = NotifyStatus.Success
        notification.message = "Job Added."

        const notifiersStore = useNotifiersStore()
        notifiersStore.forceFetchNotifiers()
        notifierItem.value = Object.assign({}, notifierDefaultItem)
    } else {
        notification.status = NotifyStatus.Error
        notification.message = "Something went wrong."
    }

    showNotify(notification)
}

const editNotifier = async () => {
    const notification = {} as NotificationType
    if (!notifier.value) {
        notification.status = NotifyStatus.Error
        notification.message = "Notifier not found."
        showNotify(notification)
        return
    }

    const status = await notifierStore.patchNotifier(notifier.value?.uuid, notifierItem.value)

    if (status) {
        closeDialog()
        notification.status = NotifyStatus.Success
        notification.message = "Notifier Updated."
        refreshJob()
    } else {
        notification.status = NotifyStatus.Error
        notification.message = "Something went wrong."
    }
    showNotify(notification)
}


const refreshJob = () => {
    if (notifier.value) {
        const notifierJobsStore = useNotifierJobsStore()
        notifierJobsStore.fetchNotifierJobs(notifier.value?.uuid, true)

        const notifierHistoryStore = useNotifierHistoryStore()
        notifierHistoryStore.fetchHistory(notifier.value?.uuid, true)

        notifierStore.fetchNotifierDelivery(notifier.value?.uuid, true)
    }
}

const testNotifier = () => {
    const notification = {} as NotificationType

    // @ts-ignore
    addEditNotifierForm.value?.validate().then(async (success: Boolean) => {
        if (success) {
            try {
                testBareNotifierLoading.value = true
                await notifiersApi.testBareNotifier(notifierItem.value)
                notifierItem.value.valid = true
            } catch (err: unknown) {
                notification.status = NotifyStatus.Error
                notification.message = `Test Failed: ${getErrorMessage(err)}`
                showNotify(notification)
            } finally {
                testBareNotifierLoading.value = false
            }
        }
    })
}

const notifier = computed(() => {
    return notifierStore.getNotifier
})

watch(() => notifier.value, () => {
    if (props.isEdit) {
        loadJob()
    }
})

const loadJob = () => {
    if (props.isEdit) {
        if (notifier.value) {
            notifierItem.value = Object.assign({}, notifier.value)
        }
    }
}

onMounted(() => {
    loadJob()
})
</script>