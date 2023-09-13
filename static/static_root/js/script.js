class NormalWindow {
  constructor(data, table) {
    this.table_div = document.querySelector(table);
    this.table = document.createElement("table")
    this.data1 = data;
    this.data = Object.keys(this.data1[0]);
  }

  show_view() {
    $(this.table_div).empty()
    this.head(this.table, this.data);
    this.jadval(this.table, this.data);
    this.table_div.appendChild(this.table)
  }

  head() {
    let thead = this.table.createTHead();
    let row = thead.insertRow();
    for (let key of this.data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

  jadval() {
    for (let element of this.data1) {
      let row = this.table.insertRow();
      for (let key of Object.values(element)) {
        let cell = row.insertCell();
        let text = document.createTextNode(key);
        cell.appendChild(text);
      }
    }
  }
}

class LittleWindow {
  constructor(data, table) {
    this.data = data;
    this.table_div = document.querySelector(table);
  }

  show_view() {
    $(this.table_div).empty()
    for (let j = 0; j < this.data.length; j++) {
      var table = document.createElement("table");
      var tbody = table.createTBody();
      for (let index = 0; index < Object.keys(this.data[j]).length; index++) {
        let td_key = tbody.insertRow();
        let td_data = tbody.insertRow();
        td_key.style.fontSize = "30px";

        let v = this.data[j];

        let keys = Object.keys(v);
        let values = Object.values(v);

        let key1 = keys[index];
        let value1 = values[index];

        let text_key = document.createTextNode(key1);
        let text_value = document.createTextNode(value1);

        td_key.appendChild(text_key);
        td_data.appendChild(text_value);
      }
      table.style.margin = "10px";
      table.style.textAlign = "center";
      table.style.width = "100%";
      this.table_div.appendChild(table);
    }
  }
}

class ResponsiveTable {
  constructor(data, table) {
    this.data = data;
    this.table = table;
  }
  show_view() {
    var table;
    let el = document.querySelector(this.table);
    $(el).empty()
    if ($(window).width() > 700) {
      table = new NormalWindow(this.data, this.table).show_view();
    } else {
      table = new LittleWindow(this.data, this.table).show_view();
    }
  }
}
