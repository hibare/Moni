<template>
    <div style="max-width: 40vw">
        <div class="text-h6 q-mb-lg">API</div>
        <div class="q-pb-xs">
            <q-inner-loading showing v-if="apiTokenLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
            <q-banner inline-actions rounded class="bg-orange q-mb-md text-black" v-if="!apiToken">
                You do not have an API token. Click on <q-icon name="refresh" color="white" size="sm" /> button below to
                generate
                one
            </q-banner>
            <q-banner inline-actions rounded class="bg-primary text-white q-mb-md" v-else>
                <q-icon name="info" size="sm" /> Please keep your API token in a secure place.
            </q-banner>

            <q-input dense filled v-model="apiToken" label="API Token" readonly
                :type="apiTokenVisibility ? 'text' : 'password'">
                <template v-slot:append>
                    <q-icon :name="apiTokenVisibility ? 'visibility_off' : 'visibility'" class="cursor-pointer q-pr-sm"
                        @click="apiTokenVisibility = !apiTokenVisibility" size="xs" />
                    <q-icon name="content_copy" class="cursor-pointer" size="xs" @click="copy2Clipboard(apiToken)" />
                </template>
            </q-input>
            <div class="row q-gutter-sm q-my-md">
                <q-icon name="refresh" color="primary" size="sm" class="cursor-pointer" @click="regenerateToken">
                    <q-tooltip>Re-generate API Token</q-tooltip>
                </q-icon>
                <q-icon name="delete" color="red" size="sm" class="cursor-pointer" :disable="apiTokenDeleteLoading"
                    @click="apiTokenDeleteDialog = true">
                    <q-tooltip>Delete API Token</q-tooltip>
                </q-icon>
            </div>
        </div>
    </div>

    <q-dialog v-model="apiTokenDeleteDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-primary">Delete API Token?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to delete this API token? Deleting API token may produce unintended side-effects.
            </q-card-section>

            <q-card-actions align="right" class="q-pt-md">
                <q-btn flat label="Cancel" class="text-capitalize" v-close-popup />
                <q-btn flat label="Delete" class="text-capitalize" color="red" :loading="apiTokenDeleteLoading"
                    :disable="apiTokenDeleteLoading" @click="deleteToken" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { copy2Clipboard, getErrorMessage, showNotify } from '../../utils/utils';
import tokenApi from '../../api/token'
import { NotifyStatus } from '../../constants';
import { NotificationType } from '../../types';

const apiToken = ref<string>("")
const apiTokenLoading = ref<boolean>(false)
const apiTokenDeleteLoading = ref<boolean>(false)
const apiTokenDeleteDialog = ref<boolean>(false)
const apiTokenVisibility = ref<boolean>(false)

const regenerateToken = async () => {
    const notifications = {} as NotificationType

    try {
        apiTokenLoading.value = true
        const data = await tokenApi.regenerateAPIToken()
        apiToken.value = data.token
        notifications.status = NotifyStatus.Success
        notifications.message = "Token Regenerated"
    } catch (err: unknown) {
        notifications.status = NotifyStatus.Error
        notifications.message = `Failed to regenerate token: ${getErrorMessage(err)}`
    } finally {
        apiTokenLoading.value = false
    }
    showNotify(notifications)

}

const deleteToken = async () => {
    const notifications = {} as NotificationType

    try {
        apiTokenDeleteLoading.value = true
        await tokenApi.deleteAPIToken()
        apiToken.value = ""
        notifications.status = NotifyStatus.Error
        notifications.message = `API Token Deleted`
        apiTokenDeleteDialog.value = false
    } catch (err: unknown) {
        notifications.status = NotifyStatus.Error
        notifications.message = `Failed to delete token: ${getErrorMessage(err)}`
    } finally {
        apiTokenDeleteLoading.value = false
    }
    showNotify(notifications)
}

onMounted(async () => {
    const notifications = {} as NotificationType

    try {
        apiTokenLoading.value = true
        const data = await tokenApi.getAPIToken()
        apiToken.value = data.token
    } catch (err: unknown) {
        notifications.status = NotifyStatus.Error
        notifications.message = `Failed to fetch token: ${getErrorMessage(err)}`
        showNotify(notifications)
    } finally {
        apiTokenLoading.value = false
    }
})
</script>