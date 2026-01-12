import React from "react";
import { Table, Tag } from "antd";
import { List, useTable } from "@refinedev/antd";

interface IOrder {
  id: number;
  adresse: string;
  type: string;
  ordre_passage: number;
}

export const OrderList: React.FC = () => {
  // On garde TA structure qui marche, on ajoute juste le filtre demandé
  const { tableProps } = useTable<IOrder>({
    resource: "orders",
    // Ajout de la propriété demandée dans tes instructions
    filters: {
      permanent: [
        {
          field: "type",
          operator: "eq",
          value: "Livraison",
        },
      ],
    },
    pagination: {
      mode: "off",
    },
  });

  return (
    <List title="Feuille de Route - Travel Order Resolver">
      <Table {...tableProps} rowKey="id">
        <Table.Column
          dataIndex="ordre_passage"
          title="Rang"
          width={80}
          render={(value: number) => <b>{value}</b>}
        />
        <Table.Column 
          dataIndex="adresse" 
          title="Adresse (Extraction NER)" 
        />
        <Table.Column
          dataIndex="type"
          title="Statut"
          render={(value: string) => (
            <Tag color="blue">{value}</Tag>
          )}
        />
      </Table>
    </List>
  );
};