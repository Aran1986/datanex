import { create } from 'zustand';

export const useFileStore = create((set, get) => ({
  files: [],
  selectedFile: null,
  uploadProgress: {},
  
  setFiles: (files) => set({ files }),
  
  addFile: (file) => set((state) => ({
    files: [file, ...state.files]
  })),
  
  updateFile: (fileId, updates) => set((state) => ({
    files: state.files.map(f => f.file_id === fileId ? { ...f, ...updates } : f)
  })),
  
  removeFile: (fileId) => set((state) => ({
    files: state.files.filter(f => f.file_id !== fileId),
    selectedFile: state.selectedFile?.file_id === fileId ? null : state.selectedFile
  })),
  
  selectFile: (file) => set({ selectedFile: file }),
  
  setUploadProgress: (fileId, progress) => set((state) => ({
    uploadProgress: { ...state.uploadProgress, [fileId]: progress }
  })),
  
  clearUploadProgress: (fileId) => set((state) => {
    const newProgress = { ...state.uploadProgress };
    delete newProgress[fileId];
    return { uploadProgress: newProgress };
  }),
}));

export const useTaskStore = create((set) => ({
  tasks: {},
  
  addTask: (taskId, taskInfo) => set((state) => ({
    tasks: { ...state.tasks, [taskId]: taskInfo }
  })),
  
  updateTask: (taskId, updates) => set((state) => ({
    tasks: {
      ...state.tasks,
      [taskId]: { ...state.tasks[taskId], ...updates }
    }
  })),
  
  removeTask: (taskId) => set((state) => {
    const newTasks = { ...state.tasks };
    delete newTasks[taskId];
    return { tasks: newTasks };
  }),
  
  clearCompletedTasks: () => set((state) => {
    const newTasks = {};
    Object.entries(state.tasks).forEach(([id, task]) => {
      if (task.status !== 'SUCCESS' && task.status !== 'FAILURE') {
        newTasks[id] = task;
      }
    });
    return { tasks: newTasks };
  }),
}));

export const useUIStore = create((set) => ({
  sidebarOpen: true,
  theme: 'light',
  notifications: [],
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  
  setTheme: (theme) => set({ theme }),
  
  addNotification: (notification) => set((state) => ({
    notifications: [...state.notifications, {
      id: Date.now(),
      ...notification
    }]
  })),
  
  removeNotification: (id) => set((state) => ({
    notifications: state.notifications.filter(n => n.id !== id)
  })),
}));

// Location: datanex-frontend/src/store/index.js
