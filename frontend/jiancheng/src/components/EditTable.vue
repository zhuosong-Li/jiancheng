<template>
    <div class="tb-container" ref="tbContainerRef">
        <el-table :data="tableData" border @row-contextmenu="rightClick" @cell-dblclick="updateCurTarget"
            :row-class-name="tableRowClassName">
            <el-table-column v-for="(col, idx) in columnList" :prop="col.prop" :index="idx" :label="col.label">
                <template #default="{ row }">
                    <p v-show="row[col.prop].show"
                        @dblclick="$event => handleEdit(row[col.prop], col.editable, $event.target)">
                        {{ row[col.prop].content }}
                        <el-icon v-show="col.editable">
                            <Edit />
                        </el-icon>
                    </p>
                    <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" v-show="!row[col.prop].show"
                        v-model="row[col.prop].content" @blur="row[col.prop].show = true">
                    </el-input>
                </template>
            </el-table-column>
        </el-table>

        <!-- 右键菜单 -->
        <div v-show="showMenu" id="contextmenu">
            <el-button type="danger" class="hideContextMenu" circle @click="showMenu = false">
                <el-icon>
                    <Close />
                </el-icon>
            </el-button>
            <el-button size="small" type="primary" @click="addRow()">上方插入一行</el-button>
            <el-button size="small" type="primary" @click="addRow(true)">下方插入一行</el-button>
            <el-popconfirm title="确定删除该行吗？" @confirm="delRow">
                <template #reference>
                    <el-button type="primary" size="small">删除当前行</el-button>
                </template>
            </el-popconfirm>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';

const props = defineProps(
    {
        'columnList': Array,
        'tableInput': Array,
        'watchFunctions': Object
    }
);
const tableData = ref([])
const showMenu = ref(false)
const curTarget = ref({
    rowIdx: null,
    colIdx: null
})
const tbContainerRef = ref(null)

for (let i = 0; i < props.tableInput.length; i++) {
    let newRow = {}
    for (let [key, value] of Object.entries(props.tableInput[i])) {
        newRow[key] = { content: value, show: true }
    }
    tableData.value.push(newRow)
}
const initializeTable = () => {
    if (tableData.value.length === 0) {
        const firstRow = {};
        for (let i = 0; i < props.columnList.length; i++) {
            const column = props.columnList[i].prop;
            firstRow[column] = {
                content: "",
                show: true
            };
        }
        tableData.value.push(firstRow)
    }
}
onMounted(initializeTable)

Object.keys(props.watchFunctions).forEach((propName) => {
    tableData.value.forEach((row) => {
        watch(
            () => row[propName].content,
            (newVal, oldVal) => {
                props.watchFunctions[propName](newVal, oldVal, tableData.value[curTarget.value.rowIdx]);
            }
        );
    })
});

const modifiable = props.columnList.every(item => item.editable)
const handleEdit = (cell, editable, pEl) => {
    if (editable) {
        const editIputEl = Array.from(pEl.nextSibling.childNodes).find(n => ['INPUT', 'TEXTAREA'].includes(n.tagName))
        cell.show = false
        editIputEl && nextTick(() => {
            editIputEl.focus()
        })
    }
}

const updateCurTarget = (row, col) => {
    curTarget.value.rowIdx = row.rowIdx
    curTarget.value.colIdx = col.index
}
const rightClick = (row, column, $event) => {
    if (modifiable) {
        // 阻止浏览器自带的右键菜单弹出
        $event.preventDefault()
        if (column.index == null) return
        // 表格容器的位置
        const { x: tbX, y: tbY } = tbContainerRef.value.getBoundingClientRect()
        // 当前鼠标位置
        const { x: pX, y: pY } = $event
        // 定位菜单
        const ele = document.getElementById('contextmenu')
        ele.style.top = pY - tbY - 6 + 'px'
        ele.style.left = pX - tbX - 6 + 'px'
        // 边界调整
        if (window.innerWidth - 140 < pX - tbX) {
            ele.style.left = 'unset'
            ele.style.right = 0
        }
        showMenu.value = true
        // 当前目标
        updateCurTarget(row, column)
    }
}

const addRow = (isUnder) => {
    showMenu.value = false
    if (curTarget.value.rowIdx === null) return
    const idx = isUnder ? curTarget.value.rowIdx + 1 : curTarget.value.rowIdx
    const newRow = {}
    props.columnList.forEach(element => {
        newRow[element.prop] = { content: '', show: true }
    });
    tableData.value.splice(idx, 0, newRow)
}

const delRow = () => {
    showMenu.value = false
    curTarget.value.rowIdx !== null && tableData.value.splice(curTarget.value.rowIdx, 1)
    initializeTable()
}

// 添加表格行下标
const tableRowClassName = ({ row, rowIndex }) => {
    row.rowIdx = rowIndex
}

</script>

<style scoped>
.tb-container {
    position: relative;
}

#contextmenu {
    position: absolute;
    top: 0;
    left: 0;
    height: auto;
    width: auto;
    border-radius: 3px;
    border: 1px solid #999999;
    background-color: #f4f4f4;
    padding: 10px;
    z-index: 12;
}

#contextmenu button {
    display: block;
    margin: 0 0 5px;
}

.hideContextMenu {
    position: absolute;
    top: 0;
    right: 0;
}
</style>
