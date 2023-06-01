<template>
    <div style="max-width: 40vw">
        <div class="text-h6 q-mb-lg">Account</div>
        <div>
            <q-form class="q-gutter-sm" ref="accountForm">
                <q-input dense filled v-model="account.first_name" label="Firstname" lazy-rules :rules="rules.nameRules" />

                <q-input dense filled v-model="account.last_name" label="Lastname" lazy-rules :rules="rules.nameRules" />

                <q-input dense filled v-model="account.email" label="Email" lazy-rules :rules="rules.emailRules" />

                <div>
                    <q-btn flat label="Update" color="primary" :loading="accountLoading" :disable="accountLoading"
                        class="text-capitalize" @click="submit" />
                </div>
            </q-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import rules from '../../utils/rules';
import { useAuthStore } from '../../store';
import { AccountType, NotificationType } from '../../types';
import { NotifyStatus } from '../../constants';
import { showNotify } from '../../utils/utils';

const accountForm = ref(null)

const account = ref<AccountType>({
    first_name: "",
    last_name: "",
    email: ""
})

const authStore = useAuthStore()

const accountLoading = computed(() => {
    return authStore.accountLoading
})

const submit = async () => {
    const notifications = {} as NotificationType

    // @ts-ignore
    accountForm.value?.validate().then(async (success: Boolean) => {
        if (success) {
            const message = await authStore.pathAccount(account.value)

            if (message === "") {
                notifications.status = NotifyStatus.Success
                notifications.message = "Account updated"
            } else {
                notifications.status = NotifyStatus.Error
                notifications.message = message
            }
            showNotify(notifications)
        }
    })
}

onMounted(() => {
    account.value.first_name = authStore.getFirstName.value || ""
    account.value.last_name = authStore.getLastName.value || ""
    account.value.email = authStore.getEmail.value || ""
})

</script>