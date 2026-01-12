import { DataProvider } from "@refinedev/core";

const mockData = [
  {
    id: 1,
    adresse: "DEPOT",
    type: "Base",
    ordre_passage: 0
  },
  {
    id: 2,
    adresse: "r. d'Anjou",
    type: "Livraison",
    ordre_passage: 1
  },
  {
    id: 3,
    adresse: "r. de la Harpe",
    type: "Livraison",
    ordre_passage: 2
  },
  {
    id: 4,
    adresse: "r. Saint-Honoré",
    type: "Livraison",
    ordre_passage: 3
  }
];

export const jsonDataProvider = (): DataProvider => {
  return {
    getList: async () => {
      return {
        data: mockData as any,
        total: mockData.length,
      };
    },

    getOne: async ({ id }) => {
      const item = mockData.find((item) => item.id === Number(id));
      return {
        data: item as any,
      };
    },

    create: async ({ variables }) => {
      return { data: variables as any };
    },

    update: async ({ variables }) => {
      return { data: variables as any };
    },

    deleteOne: async ({ id }) => {
      return { data: { id } as any };
    },

    getApiUrl: () => "",
  };
};