<template>
    <div style="min-width: 30vw">
        <div class="text-h6 q-mb-lg">Password</div>
        <div>
            <q-form class="q-gutter-sm" ref="passwordForm">
                <q-input dense filled v-model="password.old_password" label="Current Password" lazy-rules
                    :rules="rules.emptyRule" :type="oldPasswordVisibility ? 'text' : 'password'">
                    <template v-slot:append>
                        <q-icon :name="oldPasswordVisibility ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                            @click="oldPasswordVisibility = !oldPasswordVisibility" size="xs" />
                    </template>
                </q-input>

                <q-input dense filled v-model="password.new_password" label="New Password" lazy-rules
                    :rules="rules.emptyRule" :type="newPasswordVisibility ? 'text' : 'password'">
                    <template v-slot:append>
                        <q-icon :name="newPasswordVisibility ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                            @click="newPasswordVisibility = !newPasswordVisibility" size="xs" />
                    </template></q-input>

                <q-input dense filled v-model="password.new_password_confirm" label="New Password (Confirm)" lazy-rules
                    :rules="rules.emptyRule" :type="newPasswordConfirmVisibility ? 'text' : 'password'">
                    <template v-slot:append>
                        <q-icon :name="newPasswordConfirmVisibility ? 'visibility_off' : 'visibility'"
                            class="cursor-pointer" @click="newPasswordConfirmVisibility = !newPasswordConfirmVisibility"
                            size="xs" />
                    </template></q-input>

                <div>
                    <q-btn flat label="Update" color="primary" :loading="passwordLoading" :disable="passwordLoading"
                        class="text-capitalize" @click="submit" />
                </div>
            </q-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import rules from '../../utils/rules';
import authApi from "../../api/auth";
import { NotificationType, PasswordType } from '../../types';
import { NotifyStatus } from '../../constants';
import { getErrorMessage, showNotify } from '../../utils/utils';

const password = ref<PasswordType>({
    old_password: "",
    new_password: "",
    new_password_confirm: ""
})

const oldPasswordVisibility = ref<boolean>(false)
const newPasswordVisibility = ref<boolean>(false)
const newPasswordConfirmVisibility = ref<boolean>(false)
const passwordLoading = ref<boolean>(false)
const passwordForm = ref(null)

const submit = async () => {
    const notifications = {} as NotificationType

    // @ts-ignore
    passwordForm.value?.validate().then(async (success: Boolean) => {
        if (success && password.value.new_password === password.value.new_password_confirm) {
            try {
                passwordLoading.value = true
                await authApi.changePassword(password.value)
                notifications.status = NotifyStatus.Success
                notifications.message = "Updated updated"
            } catch (err: unknown) {
                notifications.status = NotifyStatus.Error
                notifications.message = getErrorMessage(err)
            } finally {
                passwordLoading.value = false
            }

            showNotify(notifications)
        } else if (password.value.new_password !== password.value.new_password_confirm) {
            notifications.status = NotifyStatus.Warning
            notifications.message = "Passwords do not match"
            showNotify(notifications)
        }
    })
}
</script>