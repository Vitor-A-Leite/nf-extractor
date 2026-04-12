from extractor import extrair_dados_nf
import json

def main(caminho):
    
    try:
        nota = extrair_dados_nf(caminho)
        
        print("✅ Extração concluída!\n")
        print(f"NF-e nº {nota.numero} | Série: {nota.serie}")
        print(f"Emitente: {nota.emitente_nome} ({nota.emitente_cnpj})")
        print(f"Destinatário: {nota.destinatario_nome}")
        print(f"Data: {nota.data_emissao}")
        print(f"Valor total: R$ {nota.valor_total:,.2f}")
        print(f"\nItens ({len(nota.itens)}):")
        for item in nota.itens:
            print(f"  - {item.descricao}: {item.quantidade} x R${item.valor_unitario:.2f} = R${item.valor_total:.2f}")
        
        # Salva como JSON
        with open(f"./dados_extraidos/nota_extraida.json", "w", encoding="utf-8") as f:
            f.write(nota.model_dump_json(indent=2, ensure_ascii=False))
        print("\n💾 Dados salvos em nota_extraida.json")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":

    caminho = "./notas/Invoice-61SIO2OR-0001.pdf" # alterer aqui para o caminho do seu PDF

    main(caminho)