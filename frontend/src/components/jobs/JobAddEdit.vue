<template>
    <q-btn round flat :icon="isEdit ? 'edit' : 'add'" color="primary" :size="props.iconSize" @click="openDialog">
        <q-tooltip>
            Click to add a Job
        </q-tooltip>
    </q-btn>
    <q-dialog v-model="jobAddEditDialog" class="q-pa-md" persistent>
        <q-card class="q-px-lg q-pt-md" style="width: 800px; max-width: 80vw;">
            <q-inner-loading showing v-if="notifiersLoading || jobLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
            <q-card-section>
                <div class="text-h6">{{ getDialogHeader }}</div>
            </q-card-section>
            <q-card-section>
                <q-form ref="addEditJobForm">
                    <q-input dense filled v-model="jobItem.title" label="Title" lazy-rules :rules="rules.titleRule" />
                    <q-input dense filled v-model="jobItem.url" label="URL" lazy-rules :rules=rules.urlRule />
                    <span>
                        Interval <q-slider v-model="jobItem.interval" :min="5" :max="180" :step="1" label
                            :label-value="jobItem.interval + ' Min.'" color="primary" />
                    </span>

                    <div class="q-py-sm">Headers <q-icon name="add" color="primary" class="cursor-pointer q-pl-sm" size="xs"
                            @click="addHeader" />
                    </div>
                    <div class="row q-col-gutter-md q-col-gutter-y-lg " v-for="(textField, i) in headers" :key="i">
                        <div class="col-md-5">
                            <q-input dse filled v-model="textField.key" label="Key" dense lazy-rules
                                :rules=rules.emptyRule />
                        </div>
                        <div class="col-md-6">
                            <q-input filled v-model="textField.value" label="Value" dense lazy-rules
                                :rules=rules.emptyRule />
                        </div>
                        <div class="col-md-1">
                            <q-icon name="close" color="red" size="xs" class="cursor-pointer" @click="removeHeader(i)" />
                        </div>
                    </div>
                    <q-select dense filled multiple v-model="jobItem.success_status" :options="statusCodeOptions"
                        label="Status Code" lazy-rules :rules=rules.emptyRule use-input input-debounce="0" use-chips
                        @filter="filterStatusCode" class="q-pt-md">
                        <template v-slot:no-option>
                            <q-item>
                                <q-item-section class="text-grey">
                                    No results
                                </q-item-section>
                            </q-item>
                        </template>
                    </q-select>

                    <q-input dense filled v-model="jobItem.failure_threshold" label="Failure Threshold" lazy-rules
                        :rules=rules.numberRule class="q-pb-lg" />

                    <q-toggle v-model="jobItem.state" color="primary" label="Enabled" />
                    <q-toggle v-model="jobItem.verify_ssl" color="red" label="Verify SSL" />
                    <q-toggle v-model="jobItem.check_redirect" color="green" label="Check Redirect" />

                    <q-select filled multiple v-model="selectedNotifiers" :options="notifierOptions" option-value="uuid"
                        label="Notifiers" lazy-rules use-input input-debounce="0" use-chips @filter="filterNotifiers"
                        :loading="notifiersLoading" :disable="notifiersLoading" class="q-pt-md">
                        <template v-slot:selected>
                            <q-chip v-for="notifier in selectedNotifiers" dense class="q-my-none q-ml-xs q-mr-xs">
                                <q-avatar :color="NotifierTypeMap[notifier.type].color" text-color="white"
                                    :icon="NotifierTypeMap[notifier.type].icon" />
                                {{ notifier.title }}
                            </q-chip>
                        </template>
                        <template v-slot:option="scope">
                            <q-item v-bind="scope.itemProps">
                                <q-item-section avatar>
                                    <q-icon :name="NotifierTypeMap[scope.opt.type].icon"
                                        :color="NotifierTypeMap[scope.opt.type].color" size="1.2rem" />
                                </q-item-section>
                                <q-item-section>
                                    <q-item-label>{{ scope.opt.title }}</q-item-label>
                                </q-item-section>
                            </q-item>
                        </template>
                        <template v-slot:no-option>
                            <q-item>
                                <q-item-section class="text-grey">
                                    No results
                                </q-item-section>
                            </q-item>
                        </template>
                    </q-select>
                </q-form>
            </q-card-section>
            <q-card-section align="right">
                <q-btn flat label="Cancel" class="text-capitalize" v-close-popup />
                <q-btn flat color="primary" label="Submit" @click="submitJob" class="text-capitalize"
                    :disable="jobLoading" />
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { HeaderType, JobAddEditType, NotificationType, NotifierType } from '../../types';
import rules from '../../utils/rules'
import { StatusCodes, NotifierTypeMap, NotifyStatus } from "../../constants"
import { useJobNotifiersStore, useJobStore, useJobsStore, useNotifiersStore } from '../../store';
import { useJobHistoryStore } from '../../store/jobHistory';
import { showNotify } from '../../utils/utils';

const addEditJobForm = ref(null)
const jobAddEditDialog = ref<boolean>(false)
const headers = ref<HeaderType[]>([])
const statusCodeOptions = ref(StatusCodes)
const notifierOptions = ref<NotifierType[]>([])
const selectedNotifiers = ref<NotifierType[]>([])

const jobItem = ref<JobAddEditType>({
    title: "",
    url: "",
    interval: 15,
    state: true,
    verify_ssl: true,
    check_redirect: false,
    headers: {},
    notifiers: [],
    success_status: [200],
    failure_threshold: 3,
})

const jobDefaultItem: JobAddEditType = {
    title: "",
    url: "",
    interval: 15,
    state: true,
    verify_ssl: true,
    check_redirect: false,
    headers: {},
    notifiers: [],
    success_status: [200],
    failure_threshold: 3,
}

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

const getDialogHeader = computed((): string => {
    return props.isEdit ? "Edit Job" : "Add Job"
})

const openDialog = () => {
    jobAddEditDialog.value = true
}

const closeDialog = () => {
    jobAddEditDialog.value = false
}

const addHeader = () => {
    headers.value.push({
        key: "",
        value: ""
    })
}

const removeHeader = (index: number) => {
    headers.value.splice(index, 1);
}

const filterStatusCode = (val: any, update: Function) => {
    if (val === '') {
        update(() => {
            statusCodeOptions.value = StatusCodes
        })
        return
    }

    update(() => {
        const needle = val.toLowerCase()
        statusCodeOptions.value = StatusCodes.filter(v => v.toString().toLowerCase().indexOf(needle) > -1)
    })
}

const filterNotifiers = (val: any, update: Function) => {
    if (val === '') {
        update(() => {
            notifierOptions.value = notifiers.value
        })
        return
    }

    update(() => {
        const needle = val.toLowerCase()
        notifierOptions.value = notifiers.value.filter(v => v.title.toLowerCase().includes(needle) || v.type.toLowerCase().includes(needle))
    })
}

const submitJob = () => {
    // @ts-ignore
    addEditJobForm.value?.validate().then((success: Boolean) => {
        if (success) {

            jobItem.value.notifiers = []
            for (const notifier of selectedNotifiers.value) {
                jobItem.value.notifiers.push(notifier.uuid)
            }

            jobItem.value.headers = {}
            for (const header of headers.value) {
                jobItem.value.headers[header.key] = header.value
            }

            props.isEdit ? editJob() : addJob()
        }
    })
}

const addJob = async () => {
    const notification = {} as NotificationType
    const jobStore = useJobStore()
    const status = await jobStore.addJob(jobItem.value)

    if (status) {
        closeDialog()

        notification.status = NotifyStatus.Success
        notification.message = "Job Added."

        const jobsStore = useJobsStore()
        jobsStore.forceFetchJobs()
        jobItem.value = Object.assign({}, jobDefaultItem)
    } else {
        notification.status = NotifyStatus.Error
        notification.message = "Something went wrong."
    }

    showNotify(notification)
}

const editJob = async () => {
    const notification = {} as NotificationType
    if (!job.value) {
        notification.status = NotifyStatus.Error
        notification.message = "Job not found."
        showNotify(notification)
        return
    }

    const jobStore = useJobStore()
    const status = await jobStore.patchJob(job.value?.uuid, jobItem.value)

    if (status) {
        closeDialog()
        notification.status = NotifyStatus.Success
        notification.message = "Job Updated."
        refreshJob()
    } else {
        notification.status = NotifyStatus.Error
        notification.message = "Something went wrong."
    }
    showNotify(notification)
}

const notifiers = computed(() => {
    const notifierStore = useNotifiersStore()
    return notifierStore.getNotifiers
})

const notifiersLoading = computed(() => {
    const notifierStore = useNotifiersStore()
    return notifierStore.loading
})

const job = computed(() => {
    const jobStore = useJobStore()
    return jobStore.getJob
})

const jobLoading = computed(() => {
    const jobStore = useJobStore()
    return jobStore.getJobLoading
})

const refreshJob = () => {
    if (job.value) {
        const jobNotifiersStore = useJobNotifiersStore()
        jobNotifiersStore.fetchNotifiers(job.value?.uuid, true)

        const jobHistoryStore = useJobHistoryStore()
        jobHistoryStore.fetchHistory(job.value?.uuid, true)

        const jobStore = useJobStore()
        jobStore.fetchJobUptime(job.value?.uuid, true)
        jobStore.fetchJobResponseTime(job.value?.uuid, true)
    }
}

watch(() => job.value, () => {
    if (props.isEdit) {
        loadJob()
    }
})

const loadJob = () => {
    if (props.isEdit) {
        if (job.value) {
            jobItem.value = Object.assign({}, job.value)

            headers.value = []
            for (let [key, value] of Object.entries(jobItem.value.headers)) {
                headers.value.push({ key: key, value: value });
            }
            jobItem.value.headers = {};

            selectedNotifiers.value = notifiers.value.filter(obj => jobItem.value.notifiers.includes(obj.uuid));
            jobItem.value.notifiers = []
        }
    }
}

onMounted(() => {
    const notifiersStore = useNotifiersStore()
    notifiersStore.fetchNotifiers()

    loadJob()
})
</script>
