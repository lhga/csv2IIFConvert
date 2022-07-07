import com.opencsv.CSVReader
import java.io.FileReader
import java.nio.charset.StandardCharsets

const val account = "Credit Card"
const val default = "Uncleared Transactions"
const val header="!ACCNT\tNAME\tACCNTTYPE\tDESC\n" +
        "ACCNT\t\"${default}\"\tEXP\t\"${default}\"\n" +
        "\n" +
        "!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\n" +
        "!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\n" +
        "!ENDTRNS\n"

fun main() {
    val fileName = "src/main/resources/numbers.csv"
    val fr = FileReader(fileName, StandardCharsets.UTF_8)
    println(header)
    fr.use { CSVReader(fr).use { it.drop(1).forEach { line -> convertItem(line) } } }
}

fun convertItem(line: Array<String>) = println(Transaction(line).reMap().toIIF())

data class Transaction(
    val card: String,
    val transactionDate: String,
    val postDate: String,
    val description: String,
    var category: String,
    var type: String,
    val amount: String,
    val memo: String
){
    constructor( line:Array<String> ): this(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
    val PAYEE = ""
    val docnum = ""
    fun toIIF(): String = "TRNS\t\t${type}\t${transactionDate}\t\"${account}\"\t\"${PAYEE}\"\t\"${amount}\"\t\"${docnum}\"\t\"${description}\"\tN\n\r" +
            "SPL\t\t${type}\t${transactionDate}\t\"${category}\"\t\t\"${flipSign(amount)}\"\t\"${docnum}\"\t\tN"
    fun reMap() :Transaction {
        category = when (category){
            "Food & Drink" ->"Meals and Entertainment:Food & Drink"
            "Bills & Utilities" -> "Utilities:Bills & Utilities"
            "Automotive" -> "Automobile Expense:Automotive"
            "Gas" -> "Automobile Expense:Gas"
            "Office & Shipping" -> "Office Supplies:Office & Shipping"
            "Professional Services" ->"Professional Fees:Professional Services"
            else -> category
        }
        type = when (type){
            "Payment" -> "PAYMENT"
            "Return" -> "CCARD REFUND"
            else -> "CREDIT CARD"
        }
        if(type != "CREDIT CARD") category = default
        return this
    }
}
fun flipSign(a : String) : String = if(a.startsWith("-")) a.substring(1) else "-${a}"
