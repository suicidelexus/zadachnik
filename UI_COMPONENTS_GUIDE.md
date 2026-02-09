# 🎨 Руководство по UI компонентам (DaisyUI + Tailwind CSS)

## ✨ Теперь у вас есть доступ к 50+ готовым компонентам!

### 📚 Официальная документация:
- **DaisyUI**: https://daisyui.com/components/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 🔥 Самые полезные компоненты для вашего проекта:

### 1. **Кнопки (Buttons)**

```html
<!-- Основная кнопка -->
<button class="btn btn-primary">Primary Button</button>

<!-- Вторичная кнопка -->
<button class="btn btn-secondary">Secondary</button>

<!-- Кнопка с успехом -->
<button class="btn btn-success">Success</button>

<!-- Кнопка с иконкой -->
<button class="btn btn-primary">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
    </svg>
    Button
</button>

<!-- Размеры -->
<button class="btn btn-xs">Tiny</button>
<button class="btn btn-sm">Small</button>
<button class="btn btn-md">Normal</button>
<button class="btn btn-lg">Large</button>

<!-- Состояния -->
<button class="btn btn-primary loading">Loading</button>
<button class="btn btn-primary" disabled>Disabled</button>
```

---

### 2. **Модальные окна (Modals)**

```html
<!-- Кнопка для открытия -->
<button class="btn" onclick="my_modal_1.showModal()">Открыть модалку</button>

<!-- Модальное окно -->
<dialog id="my_modal_1" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Привет!</h3>
    <p class="py-4">Нажмите ESC или кнопку ниже чтобы закрыть</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Закрыть</button>
      </form>
    </div>
  </div>
</dialog>

<!-- Модалка с backdrop -->
<dialog id="my_modal_2" class="modal modal-bottom sm:modal-middle">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Внимание!</h3>
    <p class="py-4">Это важное сообщение</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn btn-primary">OK</button>
        <button class="btn">Отмена</button>
      </form>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

---

### 3. **Карточки (Cards)**

```html
<!-- Простая карточка -->
<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Название задачи</h2>
    <p>Описание задачи или детали</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Открыть</button>
    </div>
  </div>
</div>

<!-- Карточка с изображением -->
<div class="card w-96 bg-base-100 shadow-xl">
  <figure><img src="/api/placeholder/400/225" alt="Placeholder" /></figure>
  <div class="card-body">
    <h2 class="card-title">
      Задача
      <div class="badge badge-secondary">NEW</div>
    </h2>
    <p>Детали задачи</p>
    <div class="card-actions justify-end">
      <div class="badge badge-outline">High Priority</div>
      <div class="badge badge-outline">In Progress</div>
    </div>
  </div>
</div>

<!-- Компактная карточка -->
<div class="card card-compact w-96 bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Компактная карточка</h2>
    <p>Меньше отступов</p>
  </div>
</div>
```

---

### 4. **Бейджи (Badges)**

```html
<div class="badge">neutral</div>
<div class="badge badge-primary">primary</div>
<div class="badge badge-secondary">secondary</div>
<div class="badge badge-accent">accent</div>
<div class="badge badge-ghost">ghost</div>

<!-- Размеры -->
<div class="badge badge-lg">Large</div>
<div class="badge badge-md">Normal</div>
<div class="badge badge-sm">Small</div>
<div class="badge badge-xs">Tiny</div>

<!-- С обводкой -->
<div class="badge badge-outline">outline</div>
<div class="badge badge-primary badge-outline">primary</div>

<!-- В кнопке -->
<button class="btn">
  Inbox
  <div class="badge">99+</div>
</button>
```

---

### 5. **Алерты (Alerts)**

```html
<!-- Информация -->
<div class="alert alert-info">
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
  <span>Новая версия доступна!</span>
</div>

<!-- Успех -->
<div class="alert alert-success">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
  <span>Задача успешно создана!</span>
</div>

<!-- Предупреждение -->
<div class="alert alert-warning">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
  <span>Предупреждение: проверьте данные!</span>
</div>

<!-- Ошибка -->
<div class="alert alert-error">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
  <span>Ошибка! Задача не была сохранена.</span>
</div>
```

---

### 6. **Формы (Forms)**

```html
<!-- Input -->
<input type="text" placeholder="Введите текст" class="input input-bordered w-full max-w-xs" />

<!-- Input с метками -->
<label class="form-control w-full max-w-xs">
  <div class="label">
    <span class="label-text">Название задачи</span>
  </div>
  <input type="text" placeholder="Type here" class="input input-bordered w-full max-w-xs" />
  <div class="label">
    <span class="label-text-alt">Обязательное поле</span>
  </div>
</label>

<!-- Select -->
<select class="select select-bordered w-full max-w-xs">
  <option disabled selected>Выберите приоритет</option>
  <option>Low</option>
  <option>Medium</option>
  <option>High</option>
  <option>Highest</option>
</select>

<!-- Textarea -->
<textarea class="textarea textarea-bordered" placeholder="Описание"></textarea>

<!-- Checkbox -->
<div class="form-control">
  <label class="label cursor-pointer">
    <span class="label-text">Запомнить меня</span>
    <input type="checkbox" class="checkbox" />
  </label>
</div>

<!-- Radio -->
<div class="form-control">
  <label class="label cursor-pointer">
    <span class="label-text">Option 1</span>
    <input type="radio" name="radio-10" class="radio checked:bg-blue-500" checked />
  </label>
</div>

<!-- Toggle -->
<input type="checkbox" class="toggle" checked />
<input type="checkbox" class="toggle toggle-primary" checked />
<input type="checkbox" class="toggle toggle-secondary" checked />
```

---

### 7. **Выпадающие меню (Dropdown)**

```html
<div class="dropdown">
  <div tabindex="0" role="button" class="btn m-1">Click</div>
  <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
    <li><a>Item 1</a></li>
    <li><a>Item 2</a></li>
  </ul>
</div>

<!-- Dropdown с иконкой -->
<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="btn btn-circle btn-ghost">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" /></svg>
  </div>
  <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
    <li><a>Профиль</a></li>
    <li><a>Настройки</a></li>
    <li><a>Выход</a></li>
  </ul>
</div>
```

---

### 8. **Таблицы (Tables)**

```html
<div class="overflow-x-auto">
  <table class="table">
    <thead>
      <tr>
        <th></th>
        <th>Name</th>
        <th>Job</th>
        <th>Favorite Color</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>1</th>
        <td>Cy Ganderton</td>
        <td>Quality Control Specialist</td>
        <td>Blue</td>
      </tr>
      <tr class="hover">
        <th>2</th>
        <td>Hart Hagerty</td>
        <td>Desktop Support Technician</td>
        <td>Purple</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Zebra стили -->
<table class="table table-zebra">
  <!-- content -->
</table>

<!-- Компактная таблица -->
<table class="table table-xs">
  <!-- content -->
</table>
```

---

### 9. **Прогресс-бары (Progress)**

```html
<progress class="progress w-56"></progress>
<progress class="progress progress-primary w-56" value="0" max="100"></progress>
<progress class="progress progress-primary w-56" value="10" max="100"></progress>
<progress class="progress progress-primary w-56" value="40" max="100"></progress>
<progress class="progress progress-primary w-56" value="70" max="100"></progress>
<progress class="progress progress-primary w-56" value="100" max="100"></progress>

<!-- Цвета -->
<progress class="progress progress-secondary w-56" value="70" max="100"></progress>
<progress class="progress progress-accent w-56" value="70" max="100"></progress>
<progress class="progress progress-success w-56" value="70" max="100"></progress>
<progress class="progress progress-warning w-56" value="70" max="100"></progress>
<progress class="progress progress-error w-56" value="70" max="100"></progress>
```

---

### 10. **Загрузка (Loading)**

```html
<span class="loading loading-spinner loading-xs"></span>
<span class="loading loading-spinner loading-sm"></span>
<span class="loading loading-spinner loading-md"></span>
<span class="loading loading-spinner loading-lg"></span>

<!-- Разные типы -->
<span class="loading loading-spinner"></span>
<span class="loading loading-dots"></span>
<span class="loading loading-ring"></span>
<span class="loading loading-ball"></span>
<span class="loading loading-bars"></span>
<span class="loading loading-infinity"></span>

<!-- В кнопке -->
<button class="btn">
  <span class="loading loading-spinner"></span>
  loading
</button>
```

---

## 🎨 Цветовые темы DaisyUI

DaisyUI поддерживает 30+ готовых тем! Меняйте тему просто изменив атрибут `data-theme`:

```html
<!-- В теге html -->
<html data-theme="light">
<html data-theme="dark">
<html data-theme="cupcake">
<html data-theme="cyberpunk">
<html data-theme="dracula">
<html data-theme="night">
```

### Доступные темы:
- light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset

---

## 🚀 Утилиты Tailwind CSS

### Spacing (отступы)
```html
<div class="p-4">padding: 1rem</div>
<div class="m-4">margin: 1rem</div>
<div class="px-4 py-2">padding-x: 1rem, padding-y: 0.5rem</div>
<div class="mt-8">margin-top: 2rem</div>
```

### Flexbox
```html
<div class="flex items-center justify-between">
  <div>Left</div>
  <div>Right</div>
</div>

<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid
```html
<div class="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>
```

### Цвета
```html
<div class="bg-blue-500 text-white">Blue background</div>
<div class="bg-red-500 text-white">Red background</div>
<div class="bg-green-500 text-white">Green background</div>
```

### Тени
```html
<div class="shadow-sm">Small shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
```

### Скругление
```html
<div class="rounded">Rounded corners</div>
<div class="rounded-lg">Large rounded</div>
<div class="rounded-full">Fully rounded (circle)</div>
```

---

## 💡 Примеры использования в вашем проекте

### Пример: Карточка задачи с DaisyUI

```html
<div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow">
  <div class="card-body">
    <div class="flex justify-between items-start">
      <h2 class="card-title">Реализовать новую фичу</h2>
      <div class="badge badge-primary">High</div>
    </div>
    
    <p class="text-sm text-gray-600">Нужно добавить возможность экспорта в Excel</p>
    
    <div class="flex gap-2 mt-2">
      <div class="badge badge-outline">Frontend</div>
      <div class="badge badge-outline">Backend</div>
    </div>
    
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-sm btn-ghost">Детали</button>
      <button class="btn btn-sm btn-primary">Взять в работу</button>
    </div>
  </div>
</div>
```

### Пример: Модалка создания задачи

```html
<button class="btn btn-primary" onclick="task_modal.showModal()">
  Новая задача
</button>

<dialog id="task_modal" class="modal">
  <div class="modal-box w-11/12 max-w-2xl">
    <h3 class="font-bold text-lg mb-4">Создать задачу</h3>
    
    <form class="space-y-4">
      <div class="form-control">
        <label class="label">
          <span class="label-text">Название</span>
        </label>
        <input type="text" class="input input-bordered" placeholder="Введите название задачи" />
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Приоритет</span>
        </label>
        <select class="select select-bordered">
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
          <option>Highest</option>
        </select>
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Описание</span>
        </label>
        <textarea class="textarea textarea-bordered" rows="4"></textarea>
      </div>
      
      <div class="modal-action">
        <form method="dialog">
          <button class="btn btn-ghost">Отмена</button>
          <button class="btn btn-primary">Создать</button>
        </form>
      </div>
    </form>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

---

## 🎯 Быстрый старт

1. **Компоненты уже подключены** через CDN в вашем `base.html`
2. **Просто копируйте примеры** из этого файла в ваши шаблоны
3. **Документация**: https://daisyui.com/components/
4. **Tailwind docs**: https://tailwindcss.com/docs

---

## 🔥 Преимущества DaisyUI + Tailwind:

✅ **50+ готовых компонентов** из коробки
✅ **30+ цветовых тем** одной строкой
✅ **Полностью кастомизируемо** через Tailwind
✅ **Легковесно** — CSS генерируется динамически
✅ **Responsive** — всё адаптивное по умолчанию
✅ **Темная тема** — поддержка из коробки
✅ **Accessibility** — семантичная разметка

---

**Используйте эти компоненты во всех ваших проектах!** 🚀
