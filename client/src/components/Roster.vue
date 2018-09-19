<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>出勤状況</h1>
        <hr><br><br>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="startWork()">
          出勤
        </button>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="endWork()">
          退勤
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">区分</th>
              <th scope="col">日付</th>
              <th scope="col">開始</th>
              <th scope="col">終了</th>
              <th scope="col">一言メモ</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(attendance, index) in attendances" :key="index">
              <td>{{ attendance.classification }}</td>
              <td>{{ attendance.day | moment("MM/DD (ddd)")}}</td>
              <td>
                <div v-if="attendance.start">
                  {{ attendance.start | moment("HH:mm:ss") }}
               </div>
              </td>
              <td>
                <div v-if="attendance.end">
                  {{ attendance.end | moment("HH:mm:ss") }}
                </div>
              </td>
              <td>{{ attendance.memo }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.attendance-update-modal
                        @click="editAttendance(attendance)">
                        Update
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- update modal -->
    <b-modal ref="updateAttendanceModal"
              id="attendance-update-modal"
              title="Update"
              hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-classification-group"
                      label="区分"
                      label-for="form-classification-edit-input">
          <b-form-select id=form-classification-edit-input
                        type="selected"
                        :options="options"
                        v-model="updateForm.classification"
                        required
                        placeholder="出勤区分を入れて下さい">

          </b-form-select>
        </b-form-group>
        <b-form-group id="form-start-group"
                      label="開始時間"
                      label-for="form-start-input">
          <b-form-input id="form-start-time-input"
                        type="time"
                        v-model="updateForm.startTime"
                        required>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-end-group"
                      label="終了時間"
                      label-for="form-end-input">
          <b-form-input id="form-end-time-input"
                        type="time"
                        v-model="updateForm.endTime"
                        required>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-memo-group"
                      label="区分"
                      label-for="form-memo-edit-input">
          <b-form-input id=form-memo-edit-input
                        type="text"
                        v-model="updateForm.memo"
                        placeholder="メモ">
          </b-form-input>/
        </b-form-group>
        <b-button type="submit" variant="primary">更新</b-button>
        <b-button type="reset" variant="danger">リセット</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  data() {
    return {
      attendances: [],
      options: [
        { value: '出勤', text: '出勤' },
        { value: '休み', text: '休み' },
        { value: '有給', text: '有給' },
        { value: '祝日', text: '祝日' },
      ],
      updateForm: {
        id: '',
        classification: '',
        startHour: '',
        startMinute: '',
        endHour: '',
        endMinute: '',
        memo: '',
      },
    };
  },
  methods: {
    initForm() {
      this.updateForm.id = '';
      this.UpdateForm.classification = '';
      this.updateForm.startTime = '';
      this.updateForm.endTime = '';
      this.updateForm.memo = '';
    },
    getAttendances() {
      const path = 'http://localhost:5000/roster';
      axios.get(path)
        .then((res) => {
          this.attendances = res.data.attendances;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    startWork() {
      const path = 'http://localhost:5000/startWork';
      axios.post(path)
        .then(() => {
          this.getAttendances();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAttendances();
        });
    },
    endWork() {
      const path = 'http://localhost:5000/endWork';
      axios.post(path)
        .then(() => {
          this.getAttendances();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAttendances();
        });
    },
    editAttendance(attendance) {
      this.updateForm = attendance;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateAttendanceModal.hide();
      // 画面入力値取得してpayload作成
      const payload = {
        id: this.updateForm.id,
        classification: this.updateForm.classification,
        startTime: this.updateForm.startTime,
        endTime: this.updateForm.endTime,
        memo: this.updateForm.memo,
      };
      // eslint-disable-next-line
      console.log(payload);
      // eslint-disable-next-line
      console.log(this.updateForm.id);
      // api kickメソッド実行
      this.updateAttendance(payload, this.updateForm.id);
    },
    updateAttendance(payload, attendanceId) {
      const path = `http://localhost:5000/roster/${attendanceId}`;
      axios.put(path, payload)
        .then(() => {
          this.getAttendances();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAttendances();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateAttendanceModal.hide();
      this.initForm();
      this.getAttendances();
    },
  },
  created() {
    this.getAttendances();
  },
};

</script>
