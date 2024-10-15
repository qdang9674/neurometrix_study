<template>
    <div>
        <div id="admin-settings">
            <div
                :class="{ 'settings-button--active': showSettingsDropdown }"
                class="settings-button"
                @click="toggleSettingsDropdown(); this.fetchComputerName();"
            >
                <i class="fas fa-cog"></i>
            </div>
        </div>

        <transition name="fade-slide">
            <div v-if="showSettingsDropdown" class="settings-dropdown">
                <p style="text-align: left;">Settings</p>
                <div style="display: flex; align-items: center;">
                    <p style="margin-right: 16px; font-size: 12px; color: rgb(180, 180, 180)">Computer Name</p>
                    <input v-model="computerName" />
                    <button @click="saveComputerName" :disabled="!isNameChanged">Save</button>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    data() {
        return {
            showSettingsDropdown: false,
            computerName: '',
            originalName: ''
        };
    },
    computed: {
        isNameChanged() {
            return this.computerName !== this.originalName;
        }
    },
    methods: {
        toggleSettingsDropdown() {
            this.showSettingsDropdown = !this.showSettingsDropdown;
        },
        fetchComputerName() {
            if (window.api && window.api.receive) {
                window.api.send('toMain', { command: 'get-computer-name' });
                window.api.receive('fromMain', (data) => {
                    this.computerName = data.computer_name || '';
                    this.originalName = this.computerName;
                });
            }
        },
        saveComputerName() {
            if (this.isNameChanged) {
                window.api.send('toMain', { command: 'update-computer-name', computer_name: this.computerName });
                this.originalName = this.computerName;
                this.fetchComputerName();
                this.$message.success('Computer name changed successfully');
            }
        }
    },
    mounted() {
        this.fetchComputerName();
    },
    beforeUnmount() {
        this.showSettingsDropdown = false;
    }
};
</script>

<style scoped>
#admin-settings {
    position: fixed;
    top: 0;
    right: 0;
    width: 100vw;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    background-color: transparent;
    font-size: 16px;
    height: 60px;
    padding-right: 20px;
    z-index: 99;
}

.settings-button {
    transition: color 0.1s ease;
    color: white;
    cursor: pointer;
}

.settings-button:not(.settings-button--active):hover {
    color: gray;
}

.settings-button--active {
    color: rgb(77, 77, 77);
}


.settings-dropdown {
    font-size: 16px;
    background: rgba(0, 0, 0, 0.2);
    position: fixed;
    right: 20px;
    top: 64px;
    padding: 16px;
    border-radius: 8px;
    filter: drop-shadow(2px 2px 4px black);
}

.fade-slide-enter-active, .fade-slide-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from, .fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.fade-slide-enter-to, .fade-slide-leave-from {
    opacity: 1;
    transform: translateY(0);
}

input {
    width: 120px;
    margin-right: 8px;
    font-family: "Monda", sans-serif;
    background-color: rgba(255, 255, 255, 0.1);
    color: rgba(215, 215, 215, 1);
    outline: none;
    border: none;
    height: 28px;
    padding: 8px;
    border-radius: 8px;
    font-size: 12px;
}

button {
    font-family: "Monda", sans-serif;
    padding: 4px 8px;
    margin-left: 8px;
    border: none;
    border-radius: 4px;
    background-color: rgba(100, 100, 255, 0.8);
    color: white;
    font-size: 12px;
    cursor: pointer;
}
button:disabled {
    background-color: rgba(100, 100, 255, 0.4);
    cursor: not-allowed;
}
</style>
