import { createStore } from 'vuex';
import router from '../router/router';

export default createStore({
  state: {
    subjectId: localStorage.getItem('user') || null,
    currentTask: localStorage.getItem('task') || null,
    selectedEcgDevice: localStorage.getItem('ecgDevice') || null,
    isSidebarCollapsed: true,
    iotStatus: 'Offline',
    eyeStatus: 'Eye tracker disconnected',
    sensorStatus: 'ECG disconnected'
  },
  mutations: {
    setSubjectId(state, subjectId) {
      state.subjectId = subjectId;
      if (subjectId) {
        localStorage.setItem('user', subjectId);
        window.api.send('toMain', { command: 'sign-in', subjectId: subjectId });
      } else {
        localStorage.removeItem('user');
      }
    },
    setCurrentTask(state, currentTask) {
      state.currentTask = currentTask;
      if (currentTask) {
        localStorage.setItem('task', currentTask);
        window.api.send('toMain', { command: 'update-task', task: currentTask });
      } else {
        localStorage.removeItem('task');
      }
    },
    setSelectedEcgDevice(state, device) {
      state.selectedEcgDevice = device;
      if (device) {
        localStorage.setItem('ecgDevice', device);
        window.api.send('toMain', { command: 'set-ecg-device', device: device });
      } else {
        localStorage.removeItem('ecgDevice');
      }
    },
    toggleSidebar(state) {
      state.isSidebarCollapsed = !state.isSidebarCollapsed;
    },
    collapseSidebar(state) {
      state.isSidebarCollapsed = true;
    },
    setIotStatus(state, status) {
      state.iotStatus = status;
    },
    setEyeStatus(state, status) {
      state.eyeStatus = status;
    },
    setSensorStatus(state, status) {
      state.sensorStatus = status;
    }
  },
  actions: {
    login({ commit }, subjectId) {
      commit('setSubjectId', subjectId);
      commit('setSelectedEcgDevice', null);
    },
    logout({ commit }) {
      commit('setSubjectId', null);
      commit('setCurrentTask', null);
      commit('setSelectedEcgDevice', null);
      commit('collapseSidebar');
      window.api.send('toMain', { command: 'disconnect-iot' });
      window.api.send('toMain', { command: 'stop-data-collection' });
      router.push('/signin');
    },
    selectEcgDevice({ commit }, device) {
      commit('setSelectedEcgDevice', device);
    },
    toggleSidebar({ commit }) {
      commit('toggleSidebar');
    },
    updateIotStatus({ commit }, status) {
      commit('setIotStatus', status);
    }
  }
});

// update iot status
if (window.api && window.api.receive) {
  window.api.receive('fromMain', (data) => {
    const store = require('./store').default;
    if (data.iotStatus) {
      store.dispatch('updateIotStatus', data.iotStatus);
    } else if (data.error) {
      store.dispatch('updateIotStatus', `Error: ${data.error}`);
    }
  });
}
